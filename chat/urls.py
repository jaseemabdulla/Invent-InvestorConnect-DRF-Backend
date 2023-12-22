from django.urls import path
from .views import MessageList

urlpatterns = [
    path('messages/<int:receiver_id>/', MessageList.as_view()),
]