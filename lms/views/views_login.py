import os
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from allauth.socialaccount.models import SocialAccount
from lms.models import Admin, CourseAdmin, EnrolledCourse, ChatRoom, Event
from lms.models import Admin, CourseAdmin, EnrolledCourse
from django.utils.timezone import now
from django.utils import timezone
from django.db.models import Count

def login(request):
    session_data = request.session
    # Inspect session keys and values
    for key, value in session_data.items():
        print(key, value)
    return render(request, 'login.html')

def logoutfunction(request):
    logout(request)
    logout_url = "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/logout?post_logout_redirect_uri={redirect_uri}"
    # Replace {tenant_id} with your Azure Active Directory tenant ID
    # Replace {redirect_uri} with the URL to redirect the user after logout (typically your application's logout page)
    # Redirect the user to the logout URL
    redirect_uri = "http://localhost:8000"  # Replace with your actual logout URL
    logout_url = logout_url.format(tenant_id=os.getenv("MS_ID"), redirect_uri=redirect_uri)
    return redirect(logout_url)

def student_dashboard(request):
    # Get the current date and time
    current_date = now()
    user = request.user
    uid = request.user.id
    context = {}
    
    # Get avatar
    social_account = SocialAccount.objects.filter(user=user, provider='microsoft').first()
    if social_account:
        extra_data = social_account.extra_data
        avatar_url = extra_data.get('photo', {}).get('url')
        context['avatar_url'] = avatar_url

    # Get chats
    chat_rooms = ChatRoom.objects.filter(chatroomuser__user=user)
    if chat_rooms.exists():
        chat_data = []
        for chat in chat_rooms:
            chat_data.append({
                'id': chat.id,
                'name': chat.name,
                'creator': chat.creator_id
            })
        context['chats'] = chat_data
    
    # Check if user is lms admin
    context["is_admin"] = request.is_admin

    # Get enrolled course if student, else get assigned course (CourseAdmin)
    if (not request.is_admin):
        my_courses = EnrolledCourse.objects.filter(user_id=uid).select_related('course')
    else:
        admin_info = Admin.objects.get(user_id=uid)
        my_courses = CourseAdmin.objects.filter(admin_id=admin_info.admin_id).select_related('course')
    
    ongoing_courses = []
    previous_courses = []

    for enrolled_course in my_courses:
        course = enrolled_course.course
        if course.start_date <= timezone.now().date() <= course.end_date:
            ongoing_courses.append(enrolled_course)
        else:
            previous_courses.append(enrolled_course)
    
    upcoming_events = Event.objects.filter(user=request.user, end_date__gte=current_date).order_by('end_date')[:5]
    
    context['ongoing_courses'] = ongoing_courses
    context['previous_courses'] = previous_courses
    context['upcoming_events'] = upcoming_events
    
    return render(request, 'dashboard.html', context)
