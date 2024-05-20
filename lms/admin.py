from django.contrib import admin, messages
from lms.models import Admin, Course, CourseAdmin

# Empty admin to let django knows we allow adding of admin via the /admin dashboard.
@admin.register(Admin)
class AddLMSAdmin(admin.ModelAdmin):
    pass

@admin.register(Course)
class AddCourse(admin.ModelAdmin):
    pass

@admin.register(CourseAdmin)
class AddCourseAdmin(admin.ModelAdmin):
    list_display = ('admin_name', 'course_name')

    def admin_name(self, obj):
        return obj.admin
    admin_name.short_description = 'Admin'

    def course_name(self, obj):
        return obj.course
    course_name.short_description = 'Course'