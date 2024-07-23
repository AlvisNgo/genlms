from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from lms.models import Assignment, Course, EnrolledCourse, CourseAdmin, Admin
from lms.forms import AssignmentForm

@login_required
def assignment_page(request, id):
    # Check if the user has access to this course
    if request.is_admin:
        if not CourseAdmin.objects.filter(admin_id=request.admin.admin_id, course_id=id).exists():
            raise Http404("Course does not exist")
    else:
        if not EnrolledCourse.objects.filter(user_id=request.user.id, course_id=id).exists():
            raise Http404("Course does not exist")
    
    course = get_object_or_404(Course, course_id=id)
    assignments = Assignment.objects.filter(course=course)
    context = {
        'course': course,
        'assignments': assignments,
    }
    return render(request, 'assignments/assignment_page.html', context)

@login_required
def assignment_submit(request, course_id, assignment_id):
    # Check if the user has access to this course
    if request.is_admin:
        if not CourseAdmin.objects.filter(admin_id=request.admin.admin_id, course_id=course_id).exists():
            raise Http404("Course does not exist")
    else:
        if not EnrolledCourse.objects.filter(user_id=request.user.id, course_id=course_id).exists():
            raise Http404("Course does not exist")

    course = get_object_or_404(Course, course_id=course_id)
    assignment = get_object_or_404(Assignment, pk=assignment_id, course=course)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignment_page', id=course_id)
    else:
        form = AssignmentForm(instance=assignment)

    context = {
        'form': form,
        'course': course,
        'assignment': assignment,
    }
    return render(request, 'assignments/assignment_submit.html', context)
