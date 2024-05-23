from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("student/dashboard", views.student_dashboard, name="dashboard"),
    path("student/course/<int:id>", views.student_course_info, name="course"),
    path("student/course/discussionboard/<int:id>", views.discussion_board, name="discussionboard"),
    path("student/course/grades/<int:id>", views.grades, name="grades"),
    path("student/course/feedback/<int:id>", views.feedback, name="feedback"),
    path("student/dashboard/profile/", views.profile_view, name="profile"),
]
