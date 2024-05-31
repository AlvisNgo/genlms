from django import forms
from lms.models import CourseAnnouncement

class AnnouncementForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'title',
            'placeholder': 'Enter ...'
        }),
        label='Announcement Title'
    )
    
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'content',
            'rows': 12,
            'placeholder': 'Enter ...'
        }),
        label='Content'
    )

class AnnouncementEditForm(forms.ModelForm):
    class Meta:
        model = CourseAnnouncement
        fields = ['title', 'content']
        
    title = forms.CharField(
    max_length=100,
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'title',
        'placeholder': 'Enter ...',
    }),
    label='Announcement Title'
)
    content = forms.CharField(
    widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'content',
        'rows': 3,
        'placeholder': 'Enter ...'
    }),
    label='Content'
)
    def __init__(self, *args, **kwargs):
        title_value = kwargs.pop('title_value', None)
        content_value = kwargs.pop('content_value', None)

        super().__init__(*args, **kwargs)
        if title_value:
            self.fields['title'].initial = title_value
        if content_value:
            self.fields['content'].initial = content_value
        
