from django.shortcuts import render
from django.conf import settings
import os
import stripe
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import redirect
from .models import Payment
from datetime import datetime

# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeCheckoutView(APIView):
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': 'price_1OJc0SSIudetI30UL8JsBh7r',
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=f'{settings.SITE_URL}/status'+ '?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=f'{settings.SITE_URL}/status' + '?canceled=true',
            )
            return redirect(checkout_session.url)
        except stripe.error.StripeError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
class PaymentSuccessView(APIView):
    def post(self, request):
        session_id = request.data.get('session_id')
        
        try:
           # Retrieve the checkout session from Stripe
            checkout_session = stripe.checkout.Session.retrieve(session_id)

            # Retrieve the subscription details separately
            subscription_id = checkout_session.subscription
            subscription = stripe.Subscription.retrieve(subscription_id)

            # Extract subscription details from the checkout session
            subscription_data = {
                'session_id': session_id,
                'payment_status': checkout_session.payment_status,
                'amount_paid': checkout_session.amount_total / 100,  # Convert to your currency
                'subscription_status': subscription.status,
                'current_period_start': datetime.utcfromtimestamp(subscription.current_period_start),
                'current_period_end': datetime.utcfromtimestamp(subscription.current_period_end),
             
            }
            
            user_payment, created = Payment.objects.update_or_create(
                user=request.user,
                defaults=subscription_data
            )

            return Response(status=status.HTTP_200_OK)
        
        except stripe.error.StripeError as e:
            print({'error': str(e)})
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
                    

        

