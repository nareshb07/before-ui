from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404,  JsonResponse
from django.views import generic
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import FollowerSignUpForm, CreatorSignUpForm
from chats.models import ChatModel
import uuid
from .helper import send_forget_password_mail
from .models import User,User, UserProfile,Creator


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


def register(request):
    return render(request, 'register.html')


class Follower_register(CreateView):
    model = User
    form_class = FollowerSignUpForm
    template_name = 'Follower_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='chats.authentication.EmailAuthBackend')
        return redirect('/')


class Creator_register(CreateView):
    model = User
    form_class = CreatorSignUpForm
    template_name = 'creator_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='chats.authentication.EmailAuthBackend')
        return redirect('/')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user, backend='chats.authentication.EmailAuthBackend')
                    return redirect('/')
                else:
                    return HttpResponse('Disabled Account')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html', context={'form': AuthenticationForm()})


def Logout(request):
    logout(request)
    return redirect('/')


def ChangePassword(request, token):
    context = {}
    try:
        profile_obj = get_object_or_404(User, token=token)
        context = {'user_id': profile_obj.id}
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/chats/change-password/{token}/')
            if new_password != confirm_password:
                messages.success(request, 'both should be equal.')
                return redirect(f'/chats/change-password/{token}/')
            try:
                validate_password(new_password, profile_obj)
            except Exception as e:
                for error in e:
                    messages.success(request, error)
                    return redirect(f'/chats/change-password/{token}/')
            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.token = ""
            user_obj.save()
            messages.success(request, "Login with new password id")
            return redirect('/chats/login/')
    except Exception as e:
        raise Http404("url not found")
    return render(request, 'change-password.html', context)


def ForgetPassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('username')
            if not email:
                messages.success(request, 'Please Enter email')
                return redirect('/chats/forget-password/')
            if not User.objects.filter(email=email).first():
                messages.success(request, 'No user found with this username.')
                return redirect('/chats/forget-password/')
            user_obj = User.objects.get(email=email)
            token = str(uuid.uuid4())
            profile_obj = User.objects.get(email=user_obj)
            profile_obj.token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('/chats/forget-password/')
    except Exception as e:
        print(e)
    return render(request, 'forget-password.html')


@login_required
def index(request):
    try:
        UserProfile_obj = UserProfile.objects.filter(user_id=request.user.id).all().order_by('-last_message')
    except Exception as e:
        print(e)
    return render(request, 'index.html', context={'friends': UserProfile_obj})


ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.mp4','.avi','.mov','.pdf','.doc','.docx', '.html', '.txt']


@csrf_exempt
def chatPage(request, id):
    try:
        UserProfile_obj = UserProfile.objects.filter(user_id=request.user.id).all().order_by('-last_message')
    except Exception as e:
        print(e)
    try:
        UserProfile.objects.filter(Follower_id=id, user_id=request.user.id).update(message_seen=False)
    except Exception as e:
        print(e)
    user_obj = User.objects.get(id=id)
    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
    if request.method == 'POST':
        if request.FILES.get('fileInput'):
            file = request.FILES['fileInput']
            if not any(file.name.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                messages.error(request, 'Invalid file type. Only JPG, JPEG, and PNG files are allowed.')
                return JsonResponse({'success': False, 'message': 'Invalid file type.'})
            chat = ChatModel.objects.create(sender=request.user.first_name, thread_name=thread_name, file=file)
            chat.save()
            file_url = chat.file.url
            file_name = chat.file.name

            response_data = {
                'success': True,
                'message': 'File uploaded successfully.',
                'file_url': file_url,
                'file_name': file_name
                
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'success': False, 'message': 'No file provided.'})
    message_objs = ChatModel.objects.filter(thread_name=thread_name).all().order_by('timestamp')
    return render(request, 'main_chat_test.html', context={'user': user_obj, 'users': UserProfile_obj, 'msgs': message_objs})


def search(request):
    return render(request, 'search_users.html')


def search_users(request):
    search_query = request.GET.get('search', '')
    creators = Creator.objects.filter(user__first_name__icontains=search_query)
    search_results = [{'first_name': creator.user.first_name, 'last_name': creator.user.last_name,
                       'image_url': creator.user.image.url, 'id': creator.user_id, 'username': creator.user.username,
                       'profession': creator.Professional_label} for creator in creators]
    return JsonResponse(search_results, safe=False)


def creator_profile(request, id):
    creator_profile = Creator.objects.get(user_id=id)
    return render(request, 'creator_profile.html', {'profile': creator_profile})

def creator_profile(request, id):
    creator_profile = Creator.objects.get(user_id=id)
    return render(request, 'creator_profile.html', {'profile': creator_profile})

def edit_creator_profile(request):
    if request.method == 'POST':
        creator_obj = Creator.objects.get(user=request.user)
        image_obj = User.objects.get(id = request.user.id)
        if request.FILES.get('profile-pic'):
            print(request.FILES['profile-pic'])
            
            image_obj.image = request.FILES['profile-pic']
            
            
           

        if request.POST.get('profession'):
            creator_obj.Professional_label = request.POST.get('profession')
        if request.POST.get('about_me'):
            creator_obj.About = request.POST.get('about_me')
        if  request.POST.get('insta'):
            creator_obj.insta = request.POST.get('insta')
        if request.POST.get('twitter'):
            creator_obj.twitter = request.POST.get('twitter')
        if request.POST.get('youtube'):
            creator_obj.youtube = request.POST.get('youtube')
        if request.POST.get('Service'):
            creator_obj.service = request.POST.get('Service')
        if request.POST.get('name'):
            image_obj.first_name = request.POST.get('name')
            
        if request.POST.get('username'):
            image_obj.username = request.POST.get('username')
        image_obj.save()
        
        creator_obj.save()
        messages.success(request, "profile_updated")
        return redirect('/my_profile/')

    obj = Creator.objects.get(user=request.user)
    return render(request, 'edit_creator_profile.html', {'creator_profile': obj})

def my_profile(request):
    creator_profile = Creator.objects.get(user = request.user)
    return render(request, 'my_profile.html', {'profile': creator_profile})

