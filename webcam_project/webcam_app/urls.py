from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),  # Example app-specific URL
    # ... other app-specific URL patterns
]
