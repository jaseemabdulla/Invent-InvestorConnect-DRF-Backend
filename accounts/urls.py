from django.urls import path
from .views import LoginApi,SignUpApi,RefreshTokenView,AdminLoginApi,ListInvstorsApi,ListEntrepreneurApi,block_unblock_user

urlpatterns = [
    path('login/',LoginApi.as_view()),
    path('signup/',SignUpApi.as_view()),
    path('refreshToken/',RefreshTokenView.as_view()),
    path('adminLogin/',AdminLoginApi.as_view()),
    path('investorList/',ListInvstorsApi.as_view()),
    path('entrepreneurList/',ListEntrepreneurApi.as_view()),
    path('userblock/<int:user_id>',block_unblock_user),
]
