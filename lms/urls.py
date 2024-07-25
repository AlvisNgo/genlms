# lms/urls.py
from django.urls import path
from .views import views_login, views_announcement, views_content, views_course, views_discussion, views_notification, views_profile, api_generative, views_calender, views_course_admin, views_analytics, views_assignment
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

     # Profile
     path("student/dashboard/profile/",
          views_profile.profile_view, name="profile"),

     # Calender
     path('calendar/', views_calender.calendar_view, name='calendar'),
     path('calendar/events/', views_calender.get_events, name='get_events'),
     path('calendar/add/', views_calender.add_event, name='add_event'),
     path('calendar/delete/<int:event_id>/', views_calender.delete_event, name='delete_event'),


     # Threads
     path("student/course/discussion_board/thread/<int:thread_id>",
          views_discussion.thread_view, name="thread_view"),
     path("student/course/discussion_board/thread/new/<int:course_id>",
          views_discussion.thread_create, name="thread_create"),
     path("student/course/discussion_board/thread/delete/<int:thread_id>",
          views_discussion.thread_delete, name="thread_delete"),
     path("student/course/discussion_board/thread/edit/<int:thread_id>",
          views_discussion.thread_edit, name="thread_edit"),
     path("student/course/discussion_board/thread/<int:thread_id>/like",
          views_discussion.like_thread, name="like_thread"),
     path("student/course/discussion_board/thread/<int:thread_id>/mark_as_read",
          views_discussion.mark_as_read, name="mark_as_read"),

     # Posts
     path("student/course/discussion_board/thread/<int:thread_id>/post/new",
          views_discussion.post_create, name="post_create"),
     path("student/course/discussion_board/post/<int:post_id>/reply",
          views_discussion.post_reply, name="post_reply"),
     path("student/course/discussion_board/thread/<int:post_id>/post/edit",
          views_discussion.post_edit, name="post_edit"),
     path("student/course/discussion_board/thread/<int:post_id>/post/delete",
          views_discussion.post_delete, name="post_delete"),
     path("student/course/discussion_board/post/<int:post_id>/like",
          views_discussion.like_post, name="like_post"),

     # Announcement
     path("student/course/<int:id>/announcement_add", views_announcement.announcement_add, name="announcement_add"),
     path("student/course/<int:id>/announcement_edit/<int:announcement_id>", views_announcement.announcement_edit, name="announcement_edit"),
     path("student/course/<int:id>/announcement_delete/<int:announcement_id>", views_announcement.announcement_delete, name="announcement_delete"),
     path("student/course/<int:id>/announcement_view/<int:announcement_id>", views_announcement.announcement_view, name="announcement_view"),

     # Assignments
     path("student/course/<int:id>/assignment_add", views_assignment.assignment_add, name="assignment_add"),
     path("student/course/<int:course_id>/assignment_view/<int:assignment_id>", views_assignment.assignment_view, name="assignment_view"),
     path("student/course/<int:course_id>/assignment_view_submission/<int:assignment_id>", views_assignment.view_submission, name="view_submission"),
     
     # Content
     path("student/course/<int:id>/content_add", views_content.content_add, name="content_add"),
     path("student/course/<int:id>/content_edit/<int:content_id>", views_content.content_edit, name="content_edit"), 
     path("student/course/<int:id>/content_delete/<int:content_id>", views_content.content_delete, name="content_delete"), 
     path("media/<str:content_name>/", views_content.content_download, name="content_download"), 

     # Generative AI API
     path("api/generative", api_generative.generate, name="generative"),
     path("api/generate_tldr", api_generative.generate_tldr, name="generative"),

     # Course Admin
     path("student/course/<int:id>/admin/student_list", views_course_admin.student_list, name="student_list"),
     path("student/course/<int:id>/admin/admin_list", views_course_admin.admin_list, name="admin_list"),

     # Notifications
     path("api/get_notification", views_notification.get_unread, name="api_get_notification"),
     path("events", views_notification.view_all_events, name="events"),

     # Analytics
     path("analytics/content_seen/<int:content_id>", views_analytics.mark_as_seen, name="mark_as_seen"),
     path("analytics/announcement_seen/<int:announce_id>", views_analytics.mark_as_seen_announce, name="mark_as_seen_announce"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
