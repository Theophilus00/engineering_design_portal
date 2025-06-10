from django.core.mail import send_mail
from django.conf import settings

def send_review_notification(design):
    subject = f"Your Design '{design.title}' Has Been Reviewed"
    message = f"""
Dear {design.user.email},

Your design titled "{design.title}" has been reviewed.

Status: {design.get_status_display()}
Feedback: {design.review_feedback or 'No additional feedback provided.'}

Thank you,
The Review Team
"""
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [design.user.email])
