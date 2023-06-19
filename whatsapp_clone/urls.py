from django.contrib import admin
from django.urls import path, include
from payments.views import initiate_payment,payment_callback
from chats.views import index,LandingPageView ,chatPage,search_users 
from chats.views import search,login_request,creator_profile, edit_creator_profile, my_profile
                          


urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', index, name='home'),
    path('chat/<int:id>/', chatPage, name='chatPage'),
    path('search/', search_users, name='search_users'),
    path('sea/', search, name = 'search'),
    path('', LandingPageView.as_view(), name = "landingpage"),
    path("chats/", include("chats.urls")),
    path('accounts/', include('allauth.urls')),
    path('login/',login_request, name='login_main'),
    path('Creator_profile/<int:id>/', creator_profile, name='creator_profile'),
    path('paytm/initiate-payment/', initiate_payment, name='paytm-initiate-payment'),
    path('paytm/callback/', payment_callback, name='paytm-callback'),
    path('profile_edit/', edit_creator_profile, name='edit_creator_profile'),
    path('my_profile/', my_profile, name='my_profile')

    
]


from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
