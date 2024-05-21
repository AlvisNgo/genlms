from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name = "login"),
    path("student/dashboard", views.student_dashboard, name = "dashboard"),
    path("student/course/<int:id>", views.student_course_info, name = "course"),
    path("student/course/1/discussionboard", views.student_discussionboard_info, name = "discussionboard"),   
    path("student/dashboard/profile/", views.profile_view, name="profile"),
]
