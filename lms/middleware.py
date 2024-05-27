from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from lms.models import Admin

class CheckAdminMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user

        # If not authenticated, redirect to root (unless we're already in root)
        if request.path != '/' and not user.is_authenticated:
            return redirect("/")

        # Set is_admin attribute in request
        request.is_admin = Admin.objects.filter(user_id=user.id).exists()