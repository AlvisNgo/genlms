from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from lms.models import Admin, Notification, Profile

class CheckAdminMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user

        # If not authenticated, redirect to root (unless we're already in root)
        if request.path.startswith('/student') and not user.is_authenticated:
            return redirect("/")
        
        # If user is superadmin
        if request.path.startswith('/student') and user.is_superuser:
            return HttpResponseRedirect(reverse('admin_index'))

        # Set admin and is_admin attribute in request
        request.admin = Admin.objects.filter(user_id=user.id).first()
        request.is_admin = Admin.objects.filter(user_id=user.id).exists()

        # Get unread count
        request.unread_event_count = Notification.objects.filter(to=user.id, read=False).count()

def profile_picture_context_processor(request):
    return {
        'profile_picture': Profile.objects.filter(user=request.user).first().profile_picture
    }