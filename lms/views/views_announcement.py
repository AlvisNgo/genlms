from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from lms.course_annoucement import AnnouncementForm, AnnouncementEditForm
from lms.models import Admin, Course, CourseAnnouncement, EnrolledCourse
from lms.utils import add_notification

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

            # Get all students from this course
            enrolled_courses = EnrolledCourse.objects.filter(course=course_info)
            students = [enrollment.user for enrollment in enrolled_courses]
            
            for student in students:
                add_notification(student, title, f"New Announcement - {course_info.course_name}", reverse('announcement_view', args=[course_info.course_id, new_announcement.id]))

            return redirect(reverse('course', args=[id]))
    else:
        form = AnnouncementForm()
        context['form'] = form
    
    # Debugging purpose
    print(context)

    return render(request, 'announcement_add.html', context)
'''
class AnnouncementEditView(UpdateView):
    model = CourseAnnouncement
    fields = ['title', 'content']
    template_name = 'announcement_edit'
'''
def announcement_edit(request, id, announcement_id):
    context = {}

    # Check if user is admin - only admin can add new announcement
    admin_info = get_object_or_404(Admin, user_id=request.user.id) # TODO: Change to 401 status

    # Get enrolled course corresponding course id, then get course details
    course_info = get_object_or_404(Course, pk=id)
    announcement_info = get_object_or_404(CourseAnnouncement,pk=announcement_id)
    dynamic_title_value = announcement_info.title
    dynamic_content_value = announcement_info.content
    context['course_info'] = course_info
    print(request.method)
    if request.method == 'POST':
        form = AnnouncementEditForm(request.POST)
        if form.is_valid():
            # Process the form data
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            announcement_info.title = title
            announcement_info.content = content
            announcement_info.updated_at = timezone.now()
            announcement_info.save()

            return redirect(reverse('course', args=[id]))
        
    elif request.method == 'DELETE':
        announcement_info.deleted_at = timezone.now()
        announcement_info.save()
        print(announcement_info.deleted_at)

        return redirect(reverse('course', args=[id]))
    else:
        form = AnnouncementEditForm(title_value=dynamic_title_value, content_value = dynamic_content_value)
        context['form'] = form
    
    # Debugging purpose
    print(context)

    return render(request, 'announcement_edit.html', context)


def announcement_delete(request, id, announcement_id):
    context = {}

    # Check if user is admin - only admin can add new announcement
    admin_info = get_object_or_404(Admin, user_id=request.user.id) # TODO: Change to 401 status

    # Get enrolled course corresponding course id, then get course details
    course_info = get_object_or_404(Course, pk=id)
    announcement_info = get_object_or_404(CourseAnnouncement,pk=announcement_id)

    context['course_info'] = course_info
    print(request.method)
    if request.method == 'POST':

        announcement_info.deleted_at = timezone.now()
        announcement_info.save()

        return redirect(reverse('course', args=[id]))
    
    # Debugging purpose
    print(context)

    return render(request, 'announcement_delete.html', context)

def announcement_view(request, id, announcement_id):
    context = {}

    # Check if user is admin - only admin can add new announcement
    #admin_info = get_object_or_404(Admin, user_id=request.user.id) # TODO: Change to 401 status

    # Get enrolled course corresponding course id, then get course details
    course_info = get_object_or_404(Course, pk=id)
    announcement_info = get_object_or_404(CourseAnnouncement,pk=announcement_id)
    
    context['course_info'] = course_info
    context['announcement_info'] = announcement_info

    print(request.method)
    if request.method == 'POST':

        return redirect(reverse('course', args=[id]))
    
    # Debugging purpose
    print(context)

    return render(request, 'announcement_view.html', context)
    
