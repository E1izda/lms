from django.urls import path
from .views import PaymentListView, create_payment_intent, confirm_payment

app_name = 'payments'

urlpatterns = [
    path('', PaymentListView.as_view(), name='payment-list'),
    path('create-intent/<int:course_id>/', create_payment_intent, name='create-payment-intent'),
    path('confirm/<int:payment_id>/', confirm_payment, name='confirm-payment'),
]