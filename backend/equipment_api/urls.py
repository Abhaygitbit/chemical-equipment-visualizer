"""
URL Configuration for Equipment API
"""

from django.urls import path
from . import views

app_name = 'equipment_api'

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health_check'),
    
    # Dataset operations
    path('upload/', views.upload_csv, name='upload_csv'),
    path('datasets/<int:dataset_id>/', views.get_dataset, name='get_dataset'),
    path('datasets/<int:dataset_id>/summary/', views.get_summary, name='get_summary'),
    path('datasets/<int:dataset_id>/pdf/', views.generate_pdf, name='generate_pdf'),
    
    # History
    path('history/', views.get_history, name='get_history'),
]