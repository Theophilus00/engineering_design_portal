from django.urls import path
from . import views

app_name = 'designs'

urlpatterns =[
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_design, name='upload_design'),
]