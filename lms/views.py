from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount

from lms.models import EnrolledCourse

def login(request):
    return render(request, 'login.html')

def student_dashboard(request):
    user = request.user
    uid = request.user.id
    context = {}

    if not user.is_authenticated:
        return redirect("/");

    # Get avatar
    social_account = SocialAccount.objects.filter(user=user, provider='microsoft').first()
    if social_account:
        extra_data = social_account.extra_data
        avatar_url = extra_data.get('photo', {}).get('url')
        context['avatar_url'] = avatar_url
    
    # Get enrolled course
    my_courses = EnrolledCourse.objects.filter(user_id=uid).select_related('course')
    context['my_courses'] = my_courses;
    
    return render(request, 'dashboard.html', context)