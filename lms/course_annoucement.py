from django import forms

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