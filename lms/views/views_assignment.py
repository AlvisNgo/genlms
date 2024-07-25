from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models import Max
from django.utils import timezone
from lms.forms_assignment import AssignmentForm, AssignmentSubmissionForm
from lms.models import Admin, Assignment, AssignmentSubmission, Course, CourseAdmin, EnrolledCourse
from lms.utils import generate_sas_url

def assignment_add(request, id):
    context = {}

    # Check if user is admin - only admin can add new announcement
    admin_info = get_object_or_404(Admin, user_id=request.user.id) # TODO: Change to 401 status

    # Get enrolled course corresponding course id, then get course details
    course_info = get_object_or_404(Course, pk=id)
    context['course_info'] = course_info

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            # Process the form data
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            due_at = form.cleaned_data['due_at']

            new_assignment = Assignment(course=course_info, title=title, content=content, due_at=due_at)
            new_assignment.save()

            return redirect(reverse('course', args=[id]))
        else:
            return redirect(reverse('assignment_add', args=[id]))
    else:
        form = AssignmentForm()
        context['form'] = form

    return render(request, 'assignment_add.html', context)

def assignment_view(request, course_id, assignment_id):
    context = {}

    # Get course and assignment details
    course_info = get_object_or_404(Course, pk=course_id)
    assignment_info = get_object_or_404(Assignment, pk=assignment_id)

    # Only user enrolled in this course can view the course
    if request.is_admin:
        if not CourseAdmin.objects.filter(admin_id=request.admin.admin_id, course_id=course_id).exists():
            raise Http404("Course does not exist")
    else:
        if not EnrolledCourse.objects.filter(user_id=request.user.id, course_id=course_id).exists():
            raise Http404("Course does not exist")

    # Handle form submission
    if request.method == 'POST':
        # Check if any previous submissions have a grade
        submission_with_grade = AssignmentSubmission.objects.filter(
            assignment=assignment_info,
            student=request.user,
            grade__isnull=False
        ).exists()
        
        if submission_with_grade:
            # If a grade is already set, do not allow new submissions
            return HttpResponseForbidden("This assignment has already been graded.")
        else:
            form = AssignmentSubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.assignment = assignment_info
                submission.student = request.user
                submission.save()
    else:
        form = AssignmentSubmissionForm()

    # Get previous submissions for the current user and assignment
    previous_submissions = AssignmentSubmission.objects.filter(
        assignment=assignment_info,
        student=request.user
    ).order_by('-uploaded_at')
    for submission in previous_submissions:
        if submission.file:
            submission.sas_url = generate_sas_url(submission.file.name)

    context['course_info'] = course_info
    context['assignment_info'] = assignment_info
    context['form'] = form
    context['previous_submissions'] = previous_submissions

    return render(request, 'assignment_view.html', context)

def view_submission(request, course_id, assignment_id):
    context = {}

    # Get course and assignment details
    course_info = get_object_or_404(Course, pk=course_id)
    assignment_info = get_object_or_404(Assignment, pk=assignment_id)

    # Get the latest submission for each student
    latest_submissions = AssignmentSubmission.objects.filter(assignment=assignment_info).values('student').annotate(latest_submission_id=Max('id'))

    # Retrieve the actual submission objects
    submissions = AssignmentSubmission.objects.filter(id__in=[entry['latest_submission_id'] for entry in latest_submissions])

    # Generate SAS URLs for submissions
    for submission in submissions:
        if submission.file:
            submission.sas_url = generate_sas_url(submission.file.name)

    context['course_info'] = course_info
    context['assignment_info'] = assignment_info
    context['submissions'] = submissions
    context['grades'] = list(range(101))

    return render(request, 'assignment_view_submission.html', context)

def update_grade(request, submission_id):
    if request.method == 'POST':
        submission = get_object_or_404(AssignmentSubmission, pk=submission_id)
        
        # Check if user has permission to update the grade
        # Implement your permission logic here
        if not request.is_admin:
            return HttpResponseForbidden()
        
        grade = request.POST.get('grade')
        if grade is not None:
            try:
                grade = int(grade)
                if 0 <= grade <= 100:
                    submission.grade = grade
                    submission.save()
            except ValueError:
                # Handle invalid grade value
                return HttpResponseForbidden()

        return redirect('view_submission', course_id=submission.assignment.course.course_id, assignment_id=submission.assignment.id)
    else:
        return HttpResponseForbidden()