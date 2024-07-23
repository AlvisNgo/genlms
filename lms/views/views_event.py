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
        events_list = list(unread_events.values('id', 'title', 'description', 'created_at'))
        
        return JsonResponse({"success": True, "events": events_list}, safe=False, content_type='application/json')
    else:
        return JsonResponse({"success": False})
