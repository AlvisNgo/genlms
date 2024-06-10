# lms/views/views_discussion.py
from django.shortcuts import get_object_or_404, redirect, render
from lms.forms import PostForm, ThreadForm, ReplyPostForm
from django.db.models import Count
from lms.models import Course, EnrolledCourse, Post, Thread
from django.http import JsonResponse


def discussion_board(request, id):
    enrolled_course = get_object_or_404(EnrolledCourse, pk=id)
    course_info = get_object_or_404(Course, pk=enrolled_course.course_id)
    sort_option = request.GET.get('sort', 'likes')  # Sorting option

    if sort_option == 'name':
        threads = Thread.objects.filter(course=course_info).annotate(
            post_count=Count('post')).order_by('title')
    elif sort_option == 'id':
        threads = Thread.objects.filter(course=course_info).annotate(
            post_count=Count('post')).order_by('id')
    elif sort_option == 'newest':
        threads = Thread.objects.filter(course=course_info).annotate(
            post_count=Count('post')).order_by('-created_at')
    else:  # Default to sorting by likes
        threads = Thread.objects.filter(course=course_info).annotate(
            like_count=Count('likes')).order_by('-like_count')

    context = {
        'course_info': course_info,
        'threads': threads,
        'sort_option': sort_option,
    }

    return render(request, 'discussion_board.html', context)


def view_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    posts = Post.objects.filter(thread=thread).annotate(
        like_count=Count('likes')).order_by('-like_count').select_related('user')
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


def reply_post(request, post_id):
    parent_post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = ReplyPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.parent_post = parent_post
            post.thread = parent_post.thread
            post.user = request.user
            post.save()
            return redirect('view_thread', thread_id=parent_post.thread.id)
    else:
        form = ReplyPostForm()
    return render(request, 'reply_post.html', {'form': form, 'parent_post': parent_post})


def like_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.user in thread.likes.all():
        thread.likes.remove(request.user)
    else:
        thread.likes.add(request.user)
    return JsonResponse({'likes': thread.total_likes()})


def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'likes': post.likes.count(), 'liked': liked})


def mark_as_read(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    thread.is_read.add(request.user)
    return JsonResponse({'status': 'marked_as_read'})
