from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from lms.models import Admin, Event, Profile

class CheckAdminMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user

        # If not authenticated, redirect to root (unless we're already in root)
        if request.path.startswith('/student') and not user.is_authenticated:
            return redirect("/")

        # Set admin and is_admin attribute in request
        request.admin = Admin.objects.filter(user_id=user.id).first()
        request.is_admin = Admin.objects.filter(user_id=user.id).exists()

        # Get unread count
        request.unread_event_count = Event.objects.filter(to=request.user, read=False).count()

def profile_picture_context_processor(request):
    return {
        'profile_picture': Profile.objects.filter(user=request.user).first().profile_picture
    }