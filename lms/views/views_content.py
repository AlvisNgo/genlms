from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from lms.models import Course, CourseContent, Admin
from lms.forms import ContentAddForm

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
            return redirect(reverse('course', args=[id]))
    else:
        form = ContentAddForm()
        context['form'] = form
    
    return render(request, 'content_add.html', context)