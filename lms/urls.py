# lms/urls.py
from django.urls import path
from .views import views_login, views_announcement, views_course, views_discussion, views_profile

urlpatterns = [
    path("", views_login.login, name="login"),
    path("student/dashboard", views_login.student_dashboard, name="dashboard"),
    path("student/course/discussion_board/<int:id>",
         views_discussion.discussion_board, name="discussion_board"),

    # Course
    path("student/course/<int:id>",
         views_course.student_course_info, name="course"),
    path("student/course/<int:id>/grade", views_course.grades, name="grades"),
    path("student/course/<int:id>/feedback",
         views_course.feedback, name="feedback"),

    # Profile
    path("student/dashboard/profile/",
         views_profile.profile_view, name="profile"),

    # Paths for threads and posts under the discussion board
    path("student/course/discussion_board/thread/<int:thread_id>/",
         views_discussion.view_thread, name="view_thread"),
    path("student/course/discussion_board/thread/new/<int:course_id>/",
         views_discussion.create_thread, name="create_thread"),
    path("student/course/discussion_board/thread/<int:thread_id>/post/new/",
         views_discussion.create_post, name="create_post"),
    path("student/course/discussion_board/thread/<int:thread_id>/like/",
         views_discussion.like_thread, name="like_thread"),
    path("student/course/discussion_board/post/<int:post_id>/like/",
         views_discussion.like_post, name="like_post"),

    # Announcement
    path("student/course/<int:id>/announcement_add",
         views_announcement.announcement_add, name="announcement_add"),
]
