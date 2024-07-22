from django.shortcuts import get_object_or_404, render
from lms.models import Course
from django.contrib.auth.models import User

def student_list(request, id):
    user = request.user
    course_info = get_object_or_404(Course, pk=id)
    students = User.objects.filter(enrolledcourse__course_id=id)

    print(students[0].username)

    return render(request, 'admin/student_list.html', {
        "user": user,
        "course_info": course_info,
        "students": students
    })