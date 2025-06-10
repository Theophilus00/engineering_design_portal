from django.db import models
from django.conf import settings

class Design(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='designs',
        help_text="User who submitted the design."
    )
    title = models.CharField(
        max_length=255,
        help_text="Title of the design."
    )
    description = models.TextField(
        blank=True,
        help_text="Optional description of the design."
    )
    design_file = models.FileField(
        upload_to='designs/',
        help_text="Upload the design file (PDF, DOCX, etc.)."
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time the design was uploaded."
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Review status of the design."
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='reviewed_designs',
        help_text="Reviewer who reviewed the design."
    )
    review_feedback = models.TextField(
        blank=True,
        help_text="Feedback given by the reviewer."
    )
    review_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date and time when the design was reviewed."
    )

    def __str__(self):
        return self.title
