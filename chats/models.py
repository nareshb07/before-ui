from django.db import models
import datetime

from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CustomUserManager(BaseUserManager):

     def _create_user (self, email, password,first_name,last_name, **extra_fields):
     
         
        if not email:
            raise ValueError("The given email is invalid ")
        
        if not password:
            raise ValueError("password is not provided")
        
        email = self.normalize_email(email)

        user = self.model(email = email,first_name = first_name, last_name = last_name , **extra_fields)

        user.set_password(password)
        user.save(using = self._db)
        return user
     
     def create_user(self, email, password,first_name,last_name, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password,first_name,last_name, **extra_fields)

     def create_superuser(self, email, password,first_name,last_name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password,first_name,last_name, **extra_fields)

from .validator import UsernameValidator
username_validator = UsernameValidator()


from storages.backends.s3boto3 import S3Boto3Storage


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique= True, max_length=200)
   
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        }, 
    )

    image = models.ImageField(storage=S3Boto3Storage(),upload_to='media/images/',default='images/dp.png')

    is_Follower = models.BooleanField(default=False)
    
    is_Creator = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    #last_seen = models.DateTimeField(null=True, blank=True)
    token = models.CharField(max_length = 200)

    objects = CustomUserManager()

    
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email","first_name","last_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return self.first_name

class Follower(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    
    

    def __str__(self) -> str:
        return self.user.email



class Creator(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    reply_time = models.CharField(null=True, blank= True ,max_length=50)
    Charges = models.IntegerField(default=50)
    Professional_label = models.CharField(null=True, blank= True,max_length=200)
    service = models.TextField(null=True, blank= True)
    About = models.TextField(null=True, blank= True)
    insta = models.CharField(null=True, blank=True , max_length = 100)
    youtube = models.CharField(null=True, blank=True , max_length = 100)
    twitter = models.CharField(null=True, blank=True , max_length = 100)
    

    
        
    def __str__(self) -> str:
        return self.user.email






from django.db import models
#from .models import User

# Create your models here.


    



class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='User_profile')
    Follower = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='Follower_profile')
    message_seen = models.BooleanField(default=True)
    last_message = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        try :
           return f"User: {self.user.first_name} | Friend: {self.Follower.first_name}"
        except :
            return f"User: {self.user.first_name} | Friend: {None}"




class UserProfileModel(models.Model):
    user = models.OneToOneField(to=User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField( max_length=100)
    online_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.first_name 





class ChatModel(models.Model):
    sender = models.CharField(max_length=100, default=None)
    message = models.TextField(null=True, blank=True)
    file = models.FileField(storage=S3Boto3Storage(), upload_to='chat_files/',null=True, blank=True )
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        if self.message :   
           
           return self.message
        elif self.file :
            return self.file.name
    
          
    



class ChatNotification(models.Model):
    chat = models.ForeignKey(to=ChatModel, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        #return self.user.username
        return self.user.first_name
    


