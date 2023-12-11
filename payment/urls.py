from django.urls import path
from .views import StripeCheckoutView,PaymentSuccessView,PaymentValidation


urlpatterns = [
    path('createCheckoutSession/',StripeCheckoutView.as_view()),
    path('paymentSeccess/',PaymentSuccessView.as_view()),
    path('paymentValidation/',PaymentValidation.as_view()),
]
