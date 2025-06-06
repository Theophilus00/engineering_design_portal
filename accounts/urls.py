from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/', views.user_login, name='login'),
    path('resend-activation/', views.resend_activation, name='resend_activation'),
    path('logout/', views.user_logout, name='logout'),
]