from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import LoginSerializer,SignupSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

# Create your views here.


class LoginApi(APIView):
    
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data= data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']
                
                user = authenticate(email=email, password=password)
                
                
                if user is None:
                
                    data = {
                        'message': 'invalid credentials'
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST) 
                
                if user.is_blocked:
                    data = {
                        'message': 'Your account is blocked. Please contact support for assistance.'
                    }
                    return Response(data,status=status.HTTP_403_FORBIDDEN)
                
                serialized = SignupSerializer(instance=user)
                serialized_user = serialized.data 
                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': serialized_user
                }

                return Response(data,status=status.HTTP_200_OK)    
                
            data = {
                'message': 'something went wrong',
                'data' : serializer.errors
            }
                
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
            
              
        except Exception as e:
            print(e)    
            
            
            
class SignUpApi(APIView):
    
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        data = {
                'message': 'something went wrong',
                'data' : serializer.errors
            }
                
        return Response(data,status=status.HTTP_400_BAD_REQUEST)
            
        
            
        

                        