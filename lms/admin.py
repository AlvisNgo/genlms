from django.contrib import admin, messages
from lms.models import Admin

@admin.register(Admin)
class PersonAdmin(admin.ModelAdmin):
    actions = ("uppercase", "lowercase") # Necessary 