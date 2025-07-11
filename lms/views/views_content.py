import os
import mimetypes
from django.http import JsonResponse, Http404,HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from lms.models import Course, CourseContent, Admin, EnrolledCourse
from lms.forms import ContentAddForm, ContentEditForm
from django.conf import settings

def content_add(request, id):
    context = {}
    admin_info = get_object_or_404(Admin, user_id=request.user.id)
    # Get enrolled course corresponding course id, then get course details
    course_info = get_object_or_404(Course, pk=id)
    context['course_info'] = course_info
    print(request.method)
    if request.method == 'POST':
        form = ContentAddForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            files = request.FILES.get('content')
            if files:
                new_content = CourseContent(course=course_info, owner=admin_info, title=title, description=description, content=files)
            else:
                new_content = CourseContent(course=course_info, owner=admin_info, title=title, description=description)                
            new_content.save()
            return JsonResponse({"success": False})
    else:
        form = ContentAddForm()
        context['form'] = form
    
    return render(request, 'content_add.html', context)

def content_delete(request, id, content_id):
    course_info = get_object_or_404(Course, pk=id)
    content_info = get_object_or_404(CourseContent,pk=content_id)

    context = {}
    context['course_info'] = course_info
    if request.method == 'POST':
        content_info.deleted_at = timezone.now()
        content_info.save()
        return redirect(reverse('course', args=[id]))
    else:
        return render(request, 'course.html', context)
    
def content_edit(request, id, content_id):
    course_info = get_object_or_404(Course, pk=id)
    content_info = get_object_or_404(CourseContent,pk=content_id)
    admin_info = get_object_or_404(Admin, user_id=request.user.id)

    # Append course and content info to context
    context = {}
    context['course_info'] = course_info
    context['content_info'] = content_info

    original_title = content_info.title
    original_description = content_info.description

    if request.method == 'POST':
        form = ContentEditForm(request.POST, request.FILES)
        if form.is_valid():

            # Process the form data
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            files = request.FILES.get('content')
            if files:
                content_info.content = files
            content_info.title = title
            content_info.description = description
            content_info.save()
            return JsonResponse({"success": False})
            # return redirect(reverse('course', args=[id]))
    else:
        form = ContentEditForm(title_value=original_title, description_value=original_description)
        context['form'] = form
    
    return render(request, 'content_edit.html', context)

def content_download(request, content_name):        
    #file path that stores content file
    file_path = os.path.join(settings.MEDIA_ROOT, content_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
