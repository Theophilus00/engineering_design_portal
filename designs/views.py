from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Design
from .forms import DesignUploadForm
# Create your views here 

@login_required
def home(request):
    return render(request, 'designs/home.html')


@login_required
def dashboard(request):
    designs = Design.objects.filter(user=request.user)
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
