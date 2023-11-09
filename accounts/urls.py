from django.urls import path
from .views import LoginApi,SignUpApi

urlpatterns = [
    path('login/',LoginApi.as_view()),
    path('signup/',SignUpApi.as_view())
]
