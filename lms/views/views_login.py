from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.db.models import Count
from allauth.socialaccount.models import SocialAccount
from lms.models import Admin, CourseAdmin, EnrolledCourse

def login(request):
    return render(request, 'login.html')

def logoutfunction(request):
    logout(request)
    return redirect('login')

def student_dashboard(request):
    user = request.user
    uid = request.user.id
    context = {}

    # Get avatar
    social_account = SocialAccount.objects.filter(
        user=user, provider='microsoft').first()
    if social_account:
        extra_data = social_account.extra_data
        avatar_url = extra_data.get('photo', {}).get('url')
        context['avatar_url'] = avatar_url

    # Check if user is lms admin
    context["is_admin"] = request.is_admin

    # Get enrolled course if student, else get assigned course (CourseAdmin)
    if (not request.is_admin):
        my_courses = EnrolledCourse.objects.filter(
            user_id=uid).select_related('course')
        context['my_courses'] = my_courses
    else:
        admin_info = Admin.objects.get(user_id=uid)
        my_courses = CourseAdmin.objects.filter(
            admin_id=admin_info.admin_id).select_related('course')
        context['my_courses'] = my_courses
    print(context)
    return render(request, 'dashboard.html', context)
