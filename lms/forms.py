from django import forms
from django.contrib.auth.models import User
from .models import Profile
from lms.models import Thread, Post, CourseContent


class ThreadForm(forms.ModelForm):
    tags = forms.CharField(max_length=200, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Thread
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'id': 'content'}),
        }
        


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ReplyPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    profile_picture = forms.ImageField(required=False)
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say')
    ], required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'profile_picture', 'description']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile


class ContentAddForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'title',
            'placeholder': 'Title (Eg. Week 1 - OS Fundamentals)'
        }),
        label='Title'
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'description',
            'rows': 10,
            'placeholder': 'Content description...'
        }),
        label='Description'
    )

    content = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'id': 'content',
            'type':'file',
            'accept': '.png, .jpeg, .pdf, .doc, .docx, .txt',
            'upload_to':'content',
            'style': 'display: none;',
        }),
        required=False, label='Upload Files'
    )