# # lms/forms.py
# from django import forms
# from django.contrib.auth.models import User
# from .models import Profile


# class ProfileForm(forms.ModelForm):
#     # Fields for the Profile model
#     profile_picture = forms.ImageField(required=False)
#     phone = forms.CharField(max_length=15, required=False)
#     gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('prefer_not_to_say', 'Prefer not to say')], required=False)
#     description = forms.CharField(widget=forms.Textarea, required=False)
    
#     # Fields for the User model
#     first_name = forms.CharField(max_length=30, required=False)
#     last_name = forms.CharField(max_length=30, required=False)
#     email = forms.EmailField(required=False)

#     class Meta:
#         model = Profile
#         fields = ['profile_picture', 'phone', 'gender', 'description', 'first_name', 'last_name', 'email']

#     def __init__(self, *args, **kwargs):
#         super(ProfileForm, self).__init__(*args, **kwargs)
#         self.fields['first_name'].initial = self.instance.user.first_name
#         self.fields['last_name'].initial = self.instance.user.last_name
#         self.fields['email'].initial = self.instance.user.email

#     def save(self, commit=True):
#         profile = super(ProfileForm, self).save(commit=False)
#         user = profile.user
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()
#             profile.save()
#         return profile
    

from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    profile_picture = forms.ImageField(required=False)
    phone = forms.CharField(max_length=15, required=False)
    gender = forms.ChoiceField(choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say')
    ], required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'profile_picture', 'phone', 'gender', 'description']

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
