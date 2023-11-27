from django.urls import path
from .views import CreateStartup,ListPendingStartups,ListApprovedStartups,ListRejectedStartups,ListUserStartups

urlpatterns = [
    path('addStartup/',CreateStartup.as_view()),
    path('listPendingStartups/',ListPendingStartups.as_view()),
    path('listApprovedStartups/',ListApprovedStartups.as_view()),
    path('listRejectedStartups/',ListRejectedStartups.as_view()),
    path('listUserStartups/',ListUserStartups.as_view()),
]
