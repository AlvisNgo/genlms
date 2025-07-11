# lms/views/views_discussion.py
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from lms.forms import PostForm, ThreadForm, ReplyPostForm
from django.db.models import Count
from django.utils import timezone
from lms.models import Course, EnrolledCourse, Post, Thread, CourseAdmin
from django.http import JsonResponse, HttpResponseForbidden

from lms.utils import add_notification


def discussion_board(request, id):
    course_info = get_object_or_404(Course, pk=id)
    sort_option = request.GET.get('sort', 'likes')  # Sorting option

    # Validate that user has access to this course
    if request.is_admin:
        if not CourseAdmin.objects.filter(admin=request.admin, course_id=id).exists():
            return HttpResponseForbidden("Not allowed to visit this discussion board.")
    else:
        if not EnrolledCourse.objects.filter(user=request.user, course_id=id).exists():
            return HttpResponseForbidden("Not allowed to visit this discussion board.")

    if sort_option == 'name':
        threads = Thread.objects.filter(course=course_info,deleted_at__isnull=True).annotate(
            post_count=Count('post')).order_by('title')
    elif sort_option == 'id':
        threads = Thread.objects.filter(course=course_info,deleted_at__isnull=True).annotate(
            post_count=Count('post')).order_by('id')
    elif sort_option == 'newest':
        threads = Thread.objects.filter(course=course_info,deleted_at__isnull=True).annotate(
            post_count=Count('post')).order_by('-created_at')
    else:  # Default to sorting by likes
        threads = Thread.objects.filter(course=course_info,deleted_at__isnull=True).annotate(
            like_count=Count('likes')).order_by('-like_count')

    context = {
        'course_info': course_info,
        'threads': threads,
        'sort_option': sort_option,
    }

    return render(request, 'discussion_board.html', context)


def thread_view(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    posts = Post.objects.filter(thread=thread,deleted_at__isnull=True).annotate(
        like_count=Count('likes')).order_by('-like_count').select_related('user')
    course_info = get_object_or_404(Course, pk=thread.course.course_id)
    context = {'thread': thread, 'posts': posts, 'course_info': course_info}
    return render(request, 'thread_view.html', context)


def thread_create(request, course_id):
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
    return render(request, 'thread_create.html', {'form': form, 'course_info': course_info})

def thread_edit(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            thread.title = title
            thread.content = content
            thread.updated_at = timezone.now()
            thread.save()
            return redirect('discussion_board', id=thread.course_id)
    else:
        initial_data = {
            'title': thread.title,
            'content': thread.content,
        }
        form = ThreadForm(initial=initial_data, instance=thread)

    context = {
        'thread': thread,
        'form': form,
    }
    return render(request, 'thread_edit.html', context)

def thread_delete(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)

    if request.method == 'POST':

        thread.deleted_at = timezone.now()
        thread.save()

        return redirect('discussion_board', id=thread.course_id)
    
    context = {'thread': thread}
    return render(request, 'thread_delete.html', context)

def post_create(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.user = request.user
            post.save()

            if (thread.user != request.user):
                add_notification(thread.user, f"{request.user.first_name} replied to your thread.", f"New Discussion Board Reply - {thread.course.course_name}", reverse('thread_view', args=[thread.id]))
            
            return redirect('thread_view', thread_id=thread.id)
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form, 'thread': thread})


def post_reply(request, post_id):
    parent_post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = ReplyPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.parent_post = parent_post
            post.thread = parent_post.thread
            post.user = request.user
            post.save()
            
            if (parent_post.user != request.user):
                add_notification(parent_post.user, f"{request.user.first_name} replied to your post in {post.thread.title}.", f"New Discussion Board Reply - {parent_post.thread.course.course_name}", reverse('thread_view', args=[parent_post.thread.id]))
            
            return redirect('thread_view', thread_id=parent_post.thread.id)
    else:
        form = ReplyPostForm()
    return render(request, 'post_reply.html', {'form': form, 'parent_post': parent_post})

def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    thread = get_object_or_404(Thread,pk=post.thread_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            post.content = content
            post.updated_at = timezone.now()
            post.save()
            return redirect('thread_view', thread_id=post.thread_id)
    else:
        initial_data = {
            'content': post.content,
        }
        form = PostForm(initial=initial_data, instance=post)
    context = {
        'thread': thread,
        'post': post,
        'form': form,
    }
    return render(request, 'post_edit.html', context)

def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    thread = get_object_or_404(Thread,pk=post.thread_id)
    if request.method == 'POST':
        post.deleted_at = timezone.now()
        post.save()
        return redirect('thread_view', thread_id=post.thread_id) 
    context = {'thread': thread ,'post': post}
    return render(request, 'post_delete.html', context)

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
