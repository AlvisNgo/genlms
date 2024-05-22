from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("student/dashboard", views.student_dashboard, name="dashboard"),
    path("student/course/<int:id>", views.student_course_info, name="course"),
    path("student/course/discussionboard/<int:id>",
         views.discussion_board, name="discussionboard"),
    path("student/dashboard/profile/", views.profile_view, name="profile"),
    path("student/course/<int:id>/announcement_add", views.announcement_add, name="announcement_add"),
]
