from django.urls import path
from .views import CreateMentorProfile,Listmentors


urlpatterns = [
    path('createMentorProfile/',CreateMentorProfile.as_view()),
    path('listMentors/',Listmentors.as_view()),
]
