from django.urls import path
from . import views

urlpatterns = [
<<<<<<< Updated upstream
    path("", views.login, name = "login"),
    path("student/dashboard", views.student_dashboard, name = "dashboard"),
    path("student/course/<int:id>", views.student_course_info, name = "course")
]
=======
     path("", views_login.login, name="login"),
     path("student/dashboard", views_login.student_dashboard, name="dashboard"),
     path("student/course/discussion_board/<int:id>",
          views_discussion.discussion_board, name="discussion_board"),
     
     # Course
     path("student/course/<int:id>", views_course.student_course_info, name="course"),
     path("student/course/<int:id>/grade", views_course.grades, name="grades"),
     path("student/course/<int:id>/feedback", views_course.feedback, name="feedback"),
     path("student/course/<int:id>/content", views_course.content, name="content"),
          path("student/course/<int:id>/content/content_add", views_course.content_add, name="content_add"),

     # Profile
     path("student/dashboard/profile/", views_profile.profile_view, name="profile"),

     # Paths for threads and posts under the discussion board
     path("student/course/discussion_board/thread/<int:thread_id>/",
          views_discussion.view_thread, name="view_thread"),
     path("student/course/discussion_board/thread/new/<int:course_id>/",
          views_discussion.create_thread, name="create_thread"),
     path("student/course/discussion_board/thread/<int:thread_id>/post/new/",
          views_discussion.create_post, name="create_post"),
  
     # Announcement
     path("student/course/<int:id>/announcement_add", views_announcement.announcement_add, name="announcement_add"),
]
>>>>>>> Stashed changes
