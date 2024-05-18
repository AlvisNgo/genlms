from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from allauth.exceptions import ImmediateHttpResponse
from django.contrib import messages
from django.shortcuts import redirect

# By default, django-allauth disallow logging via Office365 unless it is linked. However, for our use-case, we only allow member who is in the "whitelist" to login.
# The white list is manually added via the super-admin dashboard. Hence, they do not have access to the Office365 login credentials (security duh!).
# Thus, we have to create this custom adapter to allow logging in via Office365 without linking first. This does not pose any security risk as it is a white-list based approach.

# Referenced from https://stackoverflow.com/questions/19113623/django-allauth-only-allow-users-from-a-specific-google-apps-domain

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Extract the email from the social login details
        email_address = sociallogin.user.email

        # Check if a user with this email address already exists
        existing_user = self.get_user(email=email_address)

        if existing_user:
            # If the user exists, connect the social account and log them in
            sociallogin.connect(request, existing_user)
            perform_login(request, existing_user, email_verification='optional')
        else:
            # If no such user exists, disallow the login
            messages.error(request, "No account exists with this credentials. Please contact the adminstrator for assistance.")
            raise ImmediateHttpResponse(redirect('/login'))

    def get_user(self, email):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None