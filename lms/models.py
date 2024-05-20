from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.course_name

# Composite key in Django referenced from https://stackoverflow.com/a/65005218
class EnrolledCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'course_id'], name='composite_key')
        ]
    
    def __str__(self):
        return '{} ({}) - {}'.format(self.user.email, self.user.first_name, self.course)

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.user.email, self.user.first_name)


class CourseAdmin(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['admin_id', 'course_id'], name='composite_key_courseadmin')
        ]
    
    def __str__(self):
        return '{} ({})'.format(self.admin.user.email, self.admin.user.first_name)