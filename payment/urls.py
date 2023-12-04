from django.urls import path
from .views import StripeCheckoutView


urlpatterns = [
    path('createCheckoutSession/',StripeCheckoutView.as_view()),
]
