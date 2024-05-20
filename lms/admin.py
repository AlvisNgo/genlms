from django.contrib import admin, messages
from lms.models import Admin, Course

# Empty admin to let django knows we allow adding of admin via the /admin dashboard.
@admin.register(Admin)
class AddLMSAdmin(admin.ModelAdmin):
    pass

@admin.register(Course)
class AddCourse(admin.ModelAdmin):
    pass