from django.shortcuts import get_object_or_404, render
from django.db.models import Count
from lms.models import Course, CourseAnnouncement, EnrolledCourse, Thread

def student_course_info(request, id):
    # Get enrolled course corresponding course id, then get course details
    course_info = get_object_or_404(Course, pk=id)
    courseAnnouncement_info = CourseAnnouncement.objects.filter(course=course_info).order_by('-created_at').first()
    
    context = {
        'course_info': course_info,
        'courseAnnouncement_info': courseAnnouncement_info,
    }

    print(context)
    return render(request, 'course.html', context)

def content(request, id):
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

def content_add(request, id):
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