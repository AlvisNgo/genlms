from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import Event
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
import json
from datetime import datetime




@login_required
def calendar_view(request):
    return render(request, 'calendar.html')

@login_required
def get_events(request):
    events = Event.objects.filter(user=request.user).values('id', 'title', 'description', 'start_date', 'end_date', 'color')

    event_list = []
    for event in events:
        event_list.append({
            'id': event['id'],
            'title': event['title'],
            'description': event['description'],
            'start': event['start_date'].isoformat(),
            'end': event['end_date'].isoformat(),  # Store end date
            'color': event['color']
        })
    return JsonResponse(event_list, safe=False)

@login_required
@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Event.objects.create(
            user=request.user,
            title=data['title'],
            description=data['description'],
            start_date=parse_date(data['start']),
            end_date=parse_date(data['end']),  # Store end date
            color=data['color']
        )
        return JsonResponse({'status': 'Event created successfully'})
    return JsonResponse({'status': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def delete_event(request, event_id):
    if request.method == 'DELETE':
        try:
            event = Event.objects.get(id=event_id, user=request.user)
            event.delete()
            return JsonResponse({'status': 'Event deleted successfully'})
        except Event.DoesNotExist:
            return JsonResponse({'status': 'Event not found'}, status=404)
    return JsonResponse({'status': 'Invalid request'}, status=400)


