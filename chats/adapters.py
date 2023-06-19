from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import User

class CustomAccountAdapter(DefaultAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Check if a user account already exists with the same email
        email = sociallogin.account.extra_data['email']
        user_model = User()
        try:
            user = user_model.objects.get(email=email)
            # Associate the Google account with the existing user account
            sociallogin.connect(request, user)
        except user_model.DoesNotExist:
            # No existing user account found, proceed with the regular flow
            pass

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Skip the email verification step for Google authentication
        if sociallogin.account.provider == 'google':
            sociallogin.user.email_verified = True

        
    def is_auto_signup_allowed(self, request, sociallogin):
        # Disable automatic signup for Google authentication
        return False
