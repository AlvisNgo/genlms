import json
from django.utils.html import escape
from django.http import JsonResponse
from dotenv import load_dotenv
import json
from lms.models import Event

# Load dotenv
load_dotenv()

# /api/unread_events
def get_unread(request):
    if request.method == "GET":
        # Make sure user is logged in
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"success": False, "message": "Not authenticated!"})
        
        unread_events = Event.objects.filter(to=request.user, read=False)
        unread_events_list = list(unread_events.values('id', 'title', 'description', 'link', 'created_at'))

        if len(unread_events) < 5:
            read_events = Event.objects.filter(to=request.user, read=True).order_by('-created_at')[:5-len(unread_events)]
            read_events_list = list(read_events.values('id', 'title', 'description', 'link', 'created_at'))
        else:
            read_events_list = []
        
        # Upon AJAX call, mark all events as read
        unread_events.update(read=True)
        
        return JsonResponse({"success": True, "unread_events": unread_events_list, "read_events": read_events_list}, safe=False, content_type='application/json')
    else:
        return JsonResponse({"success": False})
