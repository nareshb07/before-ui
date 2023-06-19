from django.urls import path

from . import views

from django.contrib.auth.views import PasswordChangeView ###




app_name = "chats"

urlpatterns = [
    path("",views.index, name = "index"),

    path('register/',views.register, name='register'),
    path('follower_register/',views.Follower_register.as_view(), name='follower_register'),
    path('customer_register/',views.Creator_register.as_view(), name='creator_register'),
    path('login/',views.login_request, name='login'),
    path('logout/', views.Logout ,name = 'logout'),
    path('forget-password/' , views.ForgetPassword , name="forget_password"),
    path('change-password/<token>/' , views.ChangePassword , name="change_password"),

  
]