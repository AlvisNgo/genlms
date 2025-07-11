from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('prefer_not_to_say', 'Prefer not to say')], blank=True)
    address = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='static/profile_pictures/', blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

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
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(
        User, related_name='thread_likes', blank=True)
    tags = models.CharField(max_length=200, blank=True)  # Add tags field
    is_read = models.ManyToManyField(
        User, related_name='read_threads', blank=True)  # Read/unread status

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    parent_post = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Post by {self.user.username} in {self.thread.title}"


class CourseAnnouncement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    owner = models.ForeignKey(Admin, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    is_seen = models.ManyToManyField(User, related_name='seen_announcement', blank=True)
    
    def total_seen(self):
        return self.is_seen.count()

    def __str__(self):
        return f"Announcement by {self.owner.user.username} in {self.course}"
    
class CourseContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    owner = models.ForeignKey(Admin, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.FileField(upload_to='content/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    is_seen = models.ManyToManyField(User, related_name='seen_content', blank=True)
    
    def total_seen(self):
        return self.is_seen.count()
    
    def __str__(self):
        return f"Added by {self.owner.user.username} in {self.course}"

class Notification(models.Model):
    to = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.description}"
    
class ChatRoom(models.Model):

    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ChatRoomUser(models.Model):
    chatroom = models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['chatroom', 'user'], name='composite_key_chatroomuser')
        ]
    def __str__(self):
        return f"{self.user.username} in {self.chatroom.name}"
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}'

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    color = models.CharField(max_length=7)  # To store the color hex code

    def __str__(self):
        return self.title

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    due_at = models.DateTimeField()

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    grade = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.course.course_name} - {self.student.username} - {self.uploaded_at}"
