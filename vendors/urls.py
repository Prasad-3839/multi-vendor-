from django.urls import path
from .views import create_vendor,vendor_dashboard

urlpatterns = [
    path('create/', create_vendor, name='create_vendor'),
    path('dashboard/', vendor_dashboard, name='vendor_dashboard'),
]
