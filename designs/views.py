from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Design
from .forms import DesignUploadForm, DesignReviewForm
from django.utils.timezone import now
from .utils import send_review_notification
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from .forms import DesignReviewForm
from io import BytesIO
from django.shortcuts import get_object_or_404
from django.contrib import messages
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
#from django.core.mail import message
# Create your views here 

@login_required
def home(request):
    recent_designs = Design.objects.filter(user=request.user).order_by('-uploaded_at')[:3]
    return render(request, 'designs/home.html', {
        'recent_designs': recent_designs,
    })


@login_required
def dashboard(request):
    designs = Design.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'designs/dashboard.html', {'designs': designs})


@login_required
def upload_design(request):
    if request.method == 'POST':
        form = DesignUploadForm(request.POST, request.FILES)
        if form.is_valid():
            design = form.save(commit=False)
            design.user = request.user
            design.save()
            return redirect('designs:dashboard')  # Redirect after success
    else:
        form = DesignUploadForm()

    return render(request, 'designs/upload_design.html', {'form': form})  # ✅ Always return this for GET or failed POST


@login_required
def review_feedback_pdf(request, pk):
    design = get_object_or_404(Design, pk=pk, user=request.user)
    template = get_template('designs/review_feedback_pdf.html')
    html = template.render({'design': design})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{design.title}_review.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response


def is_reviewer(user):
    return user.is_staff and user.is_superuser

@login_required
@user_passes_test(is_reviewer)
def reviewer_dashboard(request):
    pending_designs = Design.objects.filter(status='pending')
    reviewed_designs = Design.objects.exclude(status='pending').filter(review_at__isnull=False)

    return render(request, 'designs/reviewer_dashboard.html', {
        'pending_designs': pending_designs,
        'reviewed_designs': reviewed_designs,
    })


@user_passes_test(is_reviewer)
def review_design(request, pk):
    design = get_object_or_404(Design, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        feedback = request.POST.get('feedback')

        if action in ['A', 'R']: # A = Approved, R = Rejected
            design.status = action
            design.review_feedback = feedback
            design.review_at = timezone.now()
            design.reviewer = request.user
            design.save()
            messages.success(request, f"Design {design.title} has been reviewed.")
            return redirect('designs:reviewer_dashboard')
        
    return render(request, 'designs/review_design.html', {'design': design})

@login_required
def review_feedback_pdf(request, pk):
    design = get_object_or_404(Design, pk=pk)

    if request.user != design.user and not request.user.is_staff and not request.user.is_reviewer:
        return HttpResponse("Unauthorized", status=403)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Design Review Feedback")

    p.setFont("Helvetica", 12)
    y -= 40
    p.drawString(50, y, f"Title: {design.title}")
    y -= 20
    p.drawString(50, y, f"Description: {design.description}")
    y -= 20
    p.drawString(50, y, f"Design File: {design.design_file.name}")
    y -= 20
    p.drawString(50, y, f"Uploaded By: {design.user.email}")
    y -= 20
    p.drawString(50, y, f"Reviewed By: {design.reviewer.email if design.reviewer else 'N/A'}")
    y -= 20
    p.drawString(50, y, f"Status: {design.get_status_display()}")
    y -= 20
    p.drawString(50, y, f"Reviewed At: {design.review_at.strftime('%Y-%m-%d %H:%M') if design.review_at else 'N/A'}")
    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Feedback:")
    y -= 20
    p.setFont("Helvetica", 12)
    text_object = p.beginText(50, y)
    for line in design.review_feedback.splitlines():
        text_object.textLine(line)
    p.drawText(text_object)

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


@login_required
@user_passes_test(is_reviewer)
def review_design(request, pk):
    design = get_object_or_404(Design, pk=pk)

    if request.method == 'POST':
        form = DesignReviewForm(request.POST, instance=design)
        if form.is_valid():
            reviewed_design = form.save(commit=False)
            reviewed_design.reviewer = request.user
            reviewed_design.review_at = now()  # Correct field
            reviewed_design.save()
            send_review_notification(reviewed_design)  # Optional but recommended
            return redirect('designs:reviewer_dashboard')
    else:
        form = DesignReviewForm(instance=design)

    return render(request, 'designs/review_design.html', {
        'form': form,
        'design': design
    })
