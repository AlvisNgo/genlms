import os
from django.http import JsonResponse, Http404,HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from lms.models import Course, CourseContent, Admin, EnrolledCourse
from lms.forms import ContentAddForm
import mimetypes
from django.conf import settings


def content_add(request, id):
    context = {}

    # Check if user is admin - only admins can add new course content
    admin_info = get_object_or_404(Admin, user_id=request.user.id) # TODO: Change to 401 status

    # Get enrolled course corresponding course id, then get course details
    course_info = get_object_or_404(Course, pk=id)
    context['course_info'] = course_info

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

def content_download(request, content_name):
        
    #file path that stores content file
    file_path = os.path.join(settings.MEDIA_ROOT, content_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response