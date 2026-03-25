from django.urls import path
from .views import become_vendor,vendor_dashboard

urlpatterns = [
    path('become-vendor/', become_vendor, name='become_vendor'),
    path('vendor-dashboard/', vendor_dashboard, name='vendor_dashboard'),
]
