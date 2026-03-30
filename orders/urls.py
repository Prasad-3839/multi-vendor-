from django.urls import path
from . import views


urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
path('payment-failed/', views.payment_failed, name='payment_failed'),

]
