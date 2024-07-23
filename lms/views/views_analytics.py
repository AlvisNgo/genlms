from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from lms.models import CourseContent, EnrolledCourse, CourseAnnouncement

def mark_as_seen(request, content_id):
    # Check if user is admin
    if request.is_admin:
        return HttpResponseForbidden("Admins cannot mark content as seen.")
    
    content = get_object_or_404(CourseContent, pk=content_id)
    
    # Check if user is enrolled in the course
    if not EnrolledCourse.objects.filter(user_id=request.user.id, course_id=content.course).exists():
        return HttpResponseForbidden("You are not enrolled in this course.")
    
    # Mark content as seen - not toggle (disallow unread)
    if not request.user in content.is_seen.all():
        content.is_seen.add(request.user)
    
    return JsonResponse({'is_seen': content.total_seen()})

def mark_as_seen_announce(request, announce_id):
    # Check if user is admin
    if request.is_admin:
        return HttpResponseForbidden("Admins cannot mark content as seen.")
    
    announcement = get_object_or_404(CourseAnnouncement, pk=announce_id)
    
    # Check if user is enrolled in the course
    if not EnrolledCourse.objects.filter(user_id=request.user.id, course_id=announcement.course).exists():
        return HttpResponseForbidden("You are not enrolled in this course.")
    
    # Mark content as seen - not toggle (disallow unread)
    if not request.user in announcement.is_seen.all():
        announcement.is_seen.add(request.user)
    
    return JsonResponse({'is_seen': announcement.total_seen()})