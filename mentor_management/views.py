from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from accounts.models import MentorProfile,BaseUser,EntrepreneurProfile
from .serializer import MentorProfileSerializer,UserSerializer,MentorProfileGetSerializer,MentorRequestSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsEntrepreneur, IsInvestor, IsMentor
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import MentorRequest
from accounts.serializer import EntrepreneurSerializer

# Create your views here.


# creat mentor

# ===================================== Admin ===================================

class CreateMentorProfile(generics.CreateAPIView):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer
    permission_classes = [IsAdmin]
    
    def create(self, request, *args, **kwargs):
        try:
            # Extract and validate user data
            user_data = {
                'first_name':request.data.get('first_name'),
                'email':request.data.get('email'),
                'password':make_password(request.data.get('password')),
                'phone_number':request.data.get('phone_number'),
                'role': 'mentor'
            }
            print('---------------user data ------------',user_data)
            # Extract and validate mentor data
            
            mentor_data = {
                'linkedin_link':request.data.get('linkedin_link'),
                'profile_picture':request.data.get('profile_picture')
            }
            
            # Serialize and create the User instance
            
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            
            
            mentor_data['user'] = user.id
            mentor_serializer = MentorProfileSerializer(data=mentor_data)
            mentor_serializer.is_valid(raise_exception=True)
            mentor_serializer.save()
            
            data = {
                'mentor':mentor_serializer.data,
                'message': 'mentor created succesfully'
            }
            
            return Response(data,status=status.HTTP_201_CREATED)
        except Exception as e:
            if hasattr(e, 'detail') and isinstance(e.detail, dict):
                print(e.detail)
                return Response({'error': 'check your email or phone number'}, status=status.HTTP_400_BAD_REQUEST)

            print('----------------------error-----------', str(e))
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# list mentorRequest

class ListMentorRequest(generics.ListAPIView):
    queryset = MentorRequest.objects.filter(is_approved = False)
    serializer_class = MentorRequestSerializer
    permission_classes=[IsAdmin]
    
    
# assign a mentor to entrepreneur

class AssignMentor(APIView):
    permission_classes = [IsAdmin]
    def post(self,request):
        data = request.data
        enterepreneur_id = data.get('enterepreneur_id')
        mentor_id = data.get('mentor_id')
        
        entrepreneur = EntrepreneurProfile.objects.get(id = enterepreneur_id)
        mentor = MentorProfile.objects.get(id=mentor_id)
        mentor_request = MentorRequest.objects.get(entrepreneur = entrepreneur)

        if entrepreneur and mentor and mentor_request:
            entrepreneur.mentor = mentor
            entrepreneur.save()
            mentor_request.is_approved = True
            mentor_request.save()
            return Response({'message':'Assign Succesfully'},status=status.HTTP_200_OK)
        return Response({'message':'mentor not found'},status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
            
        
# ===================================== common ===================================

# list all mentors 

class Listmentors(generics.ListAPIView):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileGetSerializer
    
    
# get mentor request object 

class GetMentorRequestObj(APIView):
    permission_classes = [IsEntrepreneur]
    def get(self,request):
        user = request.user
        entrepreneur_obj = EntrepreneurProfile.objects.filter(user=user).first()
        
        if not entrepreneur_obj:
            return Response({"detail": "Entrepreneur profile not found."}, status=status.HTTP_404_NOT_FOUND)

        
        mentor_request = MentorRequest.objects.filter(entrepreneur=entrepreneur_obj).first()
            
        if mentor_request:
            serializer = MentorRequestSerializer(mentor_request)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({"detail": "MentorRequest not found for the given entrepreneur."}, status=status.HTTP_404_NOT_FOUND)
                
        
    
    
# ===================================== user ===================================   


class CreateMentorRequest(APIView):
    permission_classes = [IsEntrepreneur]
    def post(self,request):
        user = request.user
        try:
            entrepreneur_obj = EntrepreneurProfile.objects.filter(user=user).first()
            
            existing_request = MentorRequest.objects.filter(entrepreneur=entrepreneur_obj).first()
            
            if existing_request:
                return Response({'message': 'Mentor request already exists for this entrepreneur.'},status=status.HTTP_400_BAD_REQUEST)
            
            if entrepreneur_obj:
                mentor_request = MentorRequest.objects.create(entrepreneur=entrepreneur_obj)
                return Response({'message':True},status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)   
            
            
# get all entrepreneurs associated with the mentor

class ListEntrepreneursOfMentor(generics.ListAPIView):
    permission_classes = [IsMentor]
    serializer_class = EntrepreneurSerializer
    
    def get_queryset(self):
        user = self.request.user
        mentor_obj = MentorProfile.objects.get(user = user)
        entrepreneurs = EntrepreneurProfile.objects.filter(mentor = mentor_obj)
        
        return entrepreneurs
                
            
            

            
            
            
        
     
    
    
    