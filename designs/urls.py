from django.urls import path
from . import views

app_name = 'designs'

urlpatterns =[
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_design, name='upload_design'),
    path('review/<int:pk>/', views.review_design, name='review_design'),
    path('review_feedback_pdf/<int:pk>/', views.review_feedback_pdf, name='review_feedback_pdf'),
    path('reviewer/', views.reviewer_dashboard, name='reviewer_dashboard'),
    path('review/<int:pk>/', views.review_design, name='review_design'),
    path('review-pdf/<int:pk>/', views.review_feedback_pdf, name='review_feedback'),
    path('design/<int:pk>/review-pdf/', views.review_feedback_pdf, name='review_feedback_pdf'),
]