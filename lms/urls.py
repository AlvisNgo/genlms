# lms/urls.py
from django.urls import path
from .views import views_login, views_announcement, views_course, views_discussion, views_profile, api_generative, views_calender, views_assignment
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path("", views_login.login, name="login"),
     path("logout", views_login.logoutfunction, name="logout"),
     path("student/dashboard", views_login.student_dashboard, name="dashboard"),
     path("student/course/discussion_board/<int:id>",
          views_discussion.discussion_board, name="discussion_board"),
     
     # Course
     path("student/course/<int:id>", views_course.student_course_info, name="course"),
     path("student/course/<int:id>/grade", views_course.grades, name="grades"),
     path("student/course/<int:id>/feedback", views_course.feedback, name="feedback"),

     # Course
     path("student/course/<int:id>",
          views_course.student_course_info, name="course"),
     path("student/course/<int:id>/grade", views_course.grades, name="grades"),
     path("student/course/<int:id>/feedback",
          views_course.feedback, name="feedback"),

     # Profile
     path("student/dashboard/profile/",
          views_profile.profile_view, name="profile"),

     # Calender
     path('calendar/', views_calender.calendar_view, name='calendar'),
     path('calendar/events/', views_calender.get_events, name='get_events'),
     path('calendar/add/', views_calender.add_event, name='add_event'),
     path('calendar/delete/<int:event_id>/', views_calender.delete_event, name='delete_event'),


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
     path("student/course/discussion_board/post/<int:post_id>/reply/",
          views_discussion.reply_post, name="reply_post"),
     path("student/course/discussion_board/thread/<int:thread_id>/mark_as_read/",
          views_discussion.mark_as_read, name="mark_as_read"),

     # Announcement
     path("student/course/<int:id>/announcement_add", views_announcement.announcement_add, name="announcement_add"),
     path("student/course/<int:id>/announcement_edit/<int:announcement_id>", views_announcement.announcement_edit, name="announcement_edit"),
     path("student/course/<int:id>/announcement_delete/<int:announcement_id>", views_announcement.announcement_delete, name="announcement_delete"),
     path("student/course/<int:id>/announcement_view/<int:announcement_id>", views_announcement.announcement_view, name="announcement_view"),

     # Assignments
     path("student/course/<int:id>/assignment_add", views_assignment.assignment_add, name="assignment_add"),
     path("student/course/<int:course_id>/assignment_view/<int:assignment_id>", views_assignment.assignment_view, name="assignment_view"),
     path("student/course/<int:course_id>/assignment_view_submission/<int:assignment_id>", views_assignment.view_submission, name="view_submission"),

     # Generative AI API
     path("api/generative", api_generative.generate, name="generative"),
     path("api/generate_tldr", api_generative.generate_tldr, name="generative")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
