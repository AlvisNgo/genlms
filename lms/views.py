from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count
from allauth.socialaccount.models import SocialAccount

from lms.models import EnrolledCourse, Admin, CourseAdmin, Course, Thread, Post


def login(request):
    return render(request, 'login.html')


def student_dashboard(request):
    user = request.user
    uid = request.user.id
    context = {}

    if not user.is_authenticated:
        return redirect("/")

    # Get avatar
    social_account = SocialAccount.objects.filter(
        user=user, provider='microsoft').first()
    if social_account:
        extra_data = social_account.extra_data
        avatar_url = extra_data.get('photo', {}).get('url')
        context['avatar_url'] = avatar_url

    # Check if user is lms admin
    is_admin = Admin.objects.filter(user_id=uid).exists()
    context["is_admin"] = is_admin

    # Get enrolled course if student, else get assigned course (CourseAdmin)
    if (not is_admin):
        my_courses = EnrolledCourse.objects.filter(
            user_id=uid).select_related('course')
        context['my_courses'] = my_courses
    else:
        admin_info = Admin.objects.get(user_id=uid)
        my_courses = CourseAdmin.objects.filter(
            admin_id=admin_info.admin_id).select_related('course')
        context['my_courses'] = my_courses
    return render(request, 'dashboard.html', context)


def student_course_info(request, id):
    context = {}
    # Get enrolled course corresponding course id, then get course details
    course_info = Course.objects.filter(pk=id).values()
    context['course_info'] = course_info
    print(context)
    return render(request, 'course.html', context)


def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            print(f"Redirecting to profile: {profile}")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile, 'user': user})


def discussion_board(request, id):
    enrolled_course = get_object_or_404(EnrolledCourse, pk=id)
    course_info = get_object_or_404(Course, pk=enrolled_course.course_id)
    threads = Thread.objects.filter(course=course_info).annotate(
        post_count=Count('post')).prefetch_related('post_set', 'post_set__user')

    context = {
        'course_info': course_info,
        'threads': threads,
    }

    print(context)  # Debugging statement to verify context

    return render(request, 'discussionboard.html', context)


def announcement_add(request, id):
    return render(request, 'announcement_add.html')