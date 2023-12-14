from django.urls import path
from .views import CreateMentorProfile,Listmentors,CreateMentorRequest,ListMentorRequest,AssignMentor,GetMentorRequesObj


urlpatterns = [
    path('createMentorProfile/',CreateMentorProfile.as_view()),
    path('listMentors/',Listmentors.as_view()),
    path('createMentorRequest/',CreateMentorRequest.as_view()),
    path('listMentorRequest/',ListMentorRequest.as_view()),
    path('assignMentor/',AssignMentor.as_view()),
    path('getMentorRequesObj/',GetMentorRequesObj.as_view()),
]
