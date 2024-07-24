from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.db.models import Count
from lms.models import Assignment, Course, CourseAnnouncement, EnrolledCourse, CourseAdmin, Admin, CourseContent

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
    
    assignment_info = Assignment.objects.filter(course=course_info, deleted_at__isnull=True).order_by('-created_at')
    courseAnnouncement_info = CourseAnnouncement.objects.filter(course=course_info, deleted_at__isnull=True).order_by('-created_at')
    courseContent_info = CourseContent.objects.filter(course=course_info, deleted_at__isnull=True).order_by('-created_at')
    uid = request.user.id
    is_admin = Admin.objects.filter(user_id=uid).exists()
    total_students = EnrolledCourse.objects.filter(course=course_info).count()
    total_seen = CourseContent.objects.filter(course=course_info).annotate(seen_count=Count('is_seen'))
    total_seen_announce = CourseAnnouncement.objects.filter(course=course_info).annotate(seen_count=Count('is_seen'))

    context = {
        'course_info': course_info,
        'assignment_info': assignment_info,
        'courseAnnouncement_info': courseAnnouncement_info,
        'courseContent_info': courseContent_info,
        'is_admin': is_admin,
        'total_students': total_students,
        'total_seen': total_seen,
        'total_seen_announce':total_seen_announce,
    }
    
    print(context)
    return render(request, 'course.html', context)