from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from lms.course_annoucement import AnnouncementForm
from lms.models import Admin, Course, CourseAnnouncement

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
