from django.shortcuts import render
from rest_framework import generics
from accounts.models import MentorProfile,BaseUser
from .serializer import MentorProfileSerializer,UserSerializer,MentorProfileGetSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsEntrepreneur, IsInvestor
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password

# Create your views here.


# creat mentor

class CreateMentorProfile(generics.CreateAPIView):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
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
        
# list all mentors 

class Listmentors(generics.ListAPIView):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileGetSerializer
    
    
    