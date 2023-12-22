from django.urls import path
from .views import CreateMentorProfile,Listmentors,CreateMentorRequest,ListMentorRequest,AssignMentor,GetMentorRequestObj,ListEntrepreneursOfMentor


urlpatterns = [
    path('createMentorProfile/',CreateMentorProfile.as_view()),
    path('listMentors/',Listmentors.as_view()),
    path('createMentorRequest/',CreateMentorRequest.as_view()),
    path('listMentorRequest/',ListMentorRequest.as_view()),
    path('assignMentor/',AssignMentor.as_view()),
    path('getMentorRequestObj/',GetMentorRequestObj.as_view()),
    path('listEntrepreneursOfMentor/',ListEntrepreneursOfMentor.as_view()),
]
