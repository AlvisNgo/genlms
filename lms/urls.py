from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("student/dashboard", views.student_dashboard, name="dashboard"),
    path("student/course/<int:id>", views.student_course_info, name="course"),
    path("student/course/discussionboard/<int:id>",
         views.discussion_board, name="discussionboard"),
    path("student/dashboard/profile/", views.profile_view, name="profile"),

    # New paths for threads and posts under the discussion board
    path("student/course/discussionboard/thread/<int:thread_id>/",
         views.view_thread, name="view_thread"),
    path("student/course/discussionboard/thread/new/",
         views.create_thread, name="create_thread"),
    path("student/course/discussionboard/thread/<int:thread_id>/post/new/",
         views.create_post, name="create_post"),
]
