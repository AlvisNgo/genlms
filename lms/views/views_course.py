from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.db.models import Count
from lms.models import Course, CourseAnnouncement, EnrolledCourse, Thread, CourseAdmin, Admin, AssignmentSubmission 
from ..forms import AssignmentUploadForm
from django.http import HttpResponse
from datetime import timedelta
from django.utils import timezone

def student_course_info(request, id):
    # Check if they have access to this course
    if (request.is_admin):
        if not CourseAdmin.objects.filter(admin_id=request.admin.admin_id, course_id=id).exists():
            raise Http404("Course does not exist")
    else:
        if not EnrolledCourse.objects.filter(user_id=request.user.id, course_id=id).exists():
            raise Http404("Course does not exist")

    # Get enrolled course corresponding course id, then get course details
    course_info = get_object_or_404(Course, pk=id)
    
    courseAnnouncement_info = CourseAnnouncement.objects.filter(course=course_info, deleted_at__isnull=True).order_by('-created_at')
    uid = request.user.id
    is_admin = Admin.objects.filter(user_id=uid).exists()
    context = {
        'course_info': course_info,
        'courseAnnouncement_info': courseAnnouncement_info,
        'is_admin': is_admin,
    }
    
    print(context)
    return render(request, 'course.html', context)


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

def upload_assignment(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    assignment, created = AssignmentSubmission.objects.get_or_create(
        course=course,
        student=request.user,
        defaults={'deadline': timezone.now() + timedelta(days=30)}  # Set a default deadline
    )

    success_message = None
    form = AssignmentUploadForm(instance=assignment)

    if request.method == 'POST':
        if 'remove_file' in request.POST:
            assignment.file.delete()
            assignment.submitted = False
            assignment.save()
            success_message = "File has been removed."
        else:
            form = AssignmentUploadForm(request.POST, request.FILES, instance=assignment)
            if form.is_valid():
                if assignment.is_past_deadline():
                    return HttpResponse("Submission deadline has passed. You cannot submit the assignment.")
                if 'file' in request.FILES and request.FILES['file']:
                    if assignment.file and assignment.file.name != request.FILES['file'].name:
                        assignment.file.delete(save=False)  # Delete the old file if a new file is uploaded
                    assignment.file = request.FILES['file']
                    assignment.submitted = True
                    assignment.uploaded_at = timezone.now()
                    assignment.save()
                    success_message = "Submission Successful"
                else:
                    success_message = "No file has been uploaded."
            else:
                success_message = "Form is not valid."

    return render(request, 'upload_assignment.html', {
        'form': form,
        'course': course,
        'assignment': assignment,
        'success_message': success_message
    })