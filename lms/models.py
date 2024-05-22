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
            models.UniqueConstraint(
                fields=['user_id', 'course_id'], name='composite_key')
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
            models.UniqueConstraint(
                fields=['admin_id', 'course_id'], name='composite_key_courseadmin')
        ]

    def __str__(self):
        return '{} ({})'.format(self.admin.user.email, self.admin.user.first_name)


class Thread(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_post = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.user.username} in {self.thread.title}"


class CourseAnnouncement(models.Model):
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    owner = models.ForeignKey(Admin, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Announcement by {self.owner.user.username} in {self.course}"