from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from .forms import EmailAuthenticationForm, ResendActivationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Set the password
            user.is_active = False  # Deactivate account until email confirmation
            user.save()  # Save the user to the database
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email = EmailMessage(subject, message, to=[user.email])
            email.send()
            return HttpResponse('Please check your email to confirm your account.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. Please log in.')
        return redirect('accounts:login')  # Make sure 'login' is the name of your login URL
    else:
        messages.error(request, 'Activation link is invalid or expired.')
        return redirect('accounts:register')  # Redirect to signup or appropriate page


def user_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('designs:dashboard')  # Or 'home' if not namespaced
                else:
                    messages.error(request, 'Account inactive. Please verify your email.')
                    return redirect('resend_activation')
            else:
                messages.error(request, 'Invalid credentials.')
        else:
            messages.error(request, 'Invalid form submission.')
    
    else:
        form = EmailAuthenticationForm()

    # ✅ ALWAYS return a response
    return render(request, 'accounts/login.html', {'form': form})


def resend_activation(request):
    if request.method == 'POST':
        form = ResendActivationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                if not user.is_active:
                    current_site = get_current_site(request)
                    subject = 'Activate your account'
                    message = render_to_string('accounts/activation_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    })
                    email_message = EmailMessage(subject, message, to=[user.email])
                    email_message.send()
                    messages.success(request, 'Activation email resent. Check your inbox.')
                    return redirect('login')
                else:
                    messages.info(request, 'Account already active. Please log in.')
                    return redirect('login')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Email not found.')
    else:
        form = ResendActivationForm()
    return render(request, 'accounts/resend_activation.html', {'form': form})


def user_logout(request):
    logout(request)
    #messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')  # Redirect to login page after logout