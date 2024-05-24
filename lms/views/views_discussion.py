from django.shortcuts import get_object_or_404, redirect, render
from lms.forms import PostForm, ThreadForm
from django.db.models import Count
from lms.models import Course, EnrolledCourse, Post, Thread

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