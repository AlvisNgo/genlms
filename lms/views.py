from django.shortcuts import redirect, render, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from allauth.socialaccount.models import SocialAccount
from django.urls import reverse
from lms.course_annoucement import AnnouncementForm
from lms.models import EnrolledCourse, Admin, CourseAdmin, Course, Thread, Post, CourseAnnouncement
from lms.forms import ThreadForm, PostForm


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
    
    print(context)
    return render(request, 'dashboard.html', context)


def student_course_info(request, id):
    # Get enrolled course corresponding course id, then get course details
    course_info = get_object_or_404(Course, pk=id)
    courseAnnouncement_info = CourseAnnouncement.objects.filter(course=course_info).order_by('-created_at').first()
    
    context = {
        'course_info': course_info,
        'courseAnnouncement_info': courseAnnouncement_info,
    }

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
    threads = Thread.objects.filter(course=course_info).annotate(post_count=Count('post')).prefetch_related('post_set', 'post_set__user')

    context = {
        'course_info': course_info,
        'threads': threads,
    }

    print(f"Discussion Board Context: {context}")  # Debugging statement
    
    return render(request, 'discussion_board.html', context)

def view_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    posts = Post.objects.filter(thread=thread).select_related('user')
    context = {'thread': thread, 'posts': posts}
    return render(request, 'view_thread.html', context)


def create_thread(request, course_id):
    course_info = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.course_id = course_id
            thread.user = request.user
            thread.course = course_info
            thread.save()
            return redirect('discussion_board', id=course_id)
    else:
        form = ThreadForm()
    return render(request, 'create_thread.html', {'form': form, 'course_info': course_info})



def create_post(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.user = request.user
            post.save()
            return redirect('view_thread', thread_id=thread.id)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form, 'thread': thread})

def grades(request, id):
    enrolled_course = get_object_or_404(EnrolledCourse, pk=id)
    course_info = get_object_or_404(Course, pk=enrolled_course.course_id)
    threads = Thread.objects.filter(course=course_info).annotate(
        post_count=Count('post')).prefetch_related('post_set', 'post_set__user')

    context = {
        'course_info': course_info,
        'threads': threads,
    }

    print(context)  # Debugging statement to verify context

    return render(request, 'grades.html', context)

def feedback(request, id):
    enrolled_course = get_object_or_404(EnrolledCourse, pk=id)
    course_info = get_object_or_404(Course, pk=enrolled_course.course_id)
    threads = Thread.objects.filter(course=course_info).annotate(
        post_count=Count('post')).prefetch_related('post_set', 'post_set__user')

    context = {
        'course_info': course_info,
        'threads': threads,
    }

    print(context)  # Debugging statement to verify context
    return render(request, 'feedback.html', context)
def announcement_add(request, id):

    context = {}

    # Check if user is admin - only admin can add new announcement
    admin_info = get_object_or_404(Admin, user_id=request.user.id) # TODO: Change to 401 status

    # Get enrolled course corresponding course id, then get course details
    course_info = get_object_or_404(Course, pk=id)
    context['course_info'] = course_info

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            # Process the form data
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            new_announcement = CourseAnnouncement(course=course_info, owner=admin_info, title=title, content=content)
            new_announcement.save()

            return redirect(reverse('course', args=[id]))
    else:
        form = AnnouncementForm()
        context['form'] = form
    
    # Debugging purpose
    print(context)

    return render(request, 'announcement_add.html', context)
