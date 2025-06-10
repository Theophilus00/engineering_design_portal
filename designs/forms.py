from django import forms
from .models import Design

class DesignUploadForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ['title', 'description', 'design_file']

class DesignReviewForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Design.STATUS_CHOICES, label="Review Status")
    review_feedback = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write detailed feedback...'}),
        required=False,
        label="Feedback (optional)"
    )

    class Meta:
        model = Design
        fields = ['status', 'review_feedback']