from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.db.models import Count
from lms.models import Course, CourseAnnouncement, EnrolledCourse, Thread, CourseAdmin, Admin

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
    courseAnnouncement_info = CourseAnnouncement.objects.filter(course=course_info).order_by('-created_at')
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