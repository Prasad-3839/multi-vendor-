from django.urls import path
from . import views


urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('history/', views.order_history, name='history'),
    path('<int:order_id>/', views.order_detail, name='detail'),

]
