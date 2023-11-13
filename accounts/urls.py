from django.urls import path
from .views import LoginApi,SignUpApi,RefreshTokenView

urlpatterns = [
    path('login/',LoginApi.as_view()),
    path('signup/',SignUpApi.as_view()),
    path('refreshToken/',RefreshTokenView.as_view()),
]
