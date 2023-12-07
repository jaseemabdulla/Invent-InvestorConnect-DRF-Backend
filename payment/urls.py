from django.urls import path
from .views import StripeCheckoutView,PaymentSuccessView


urlpatterns = [
    path('createCheckoutSession/',StripeCheckoutView.as_view()),
    path('paymentSeccess/',PaymentSuccessView.as_view()),
]
