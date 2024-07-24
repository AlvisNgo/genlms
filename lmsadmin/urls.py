from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='admin_index'),
    path('add_users/', views.add_users, name='admin_add_users'),
    path('import_valid_rows/', views.import_valid_rows, name='import_valid_rows'),
    path('courses/', views.course_list, name='admin_course_list'),
    path('courses/<int:course_id>/enrolled-students/', views.enrolled_students, name='admin_enrolled_students'),
    path('courses/<int:course_id>/add_students/', views.add_students, name='admin_add_student_to_course'),
    path('courses/confirm_add_students/', views.confirm_add_students, name='confirm_add_students'),
    path('courses/<int:course_id>/remove_student/<int:user_id>/', views.remove_student, name='remove_student'),
]