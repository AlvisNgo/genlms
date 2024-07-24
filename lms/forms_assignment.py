from django import forms
from lms.models import Assignment, AssignmentSubmission

class AssignmentForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'title',
            'placeholder': 'Enter ...'
        }),
        label='Assignment Title'
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

    due_at = forms.DateTimeField()

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['file']