from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import LoginSerializer,SignupSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
import jwt
from django.contrib.auth import get_user_model
from django.conf import settings

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
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
                data = {
                    'token': token,
                    'user': serialized_user,
                    'message': 'login succesfully'
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
    
class RefreshTokenView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh',None)
            if not refresh_token:
                return Response({'error':'No valid refresh token'},status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                refresh = RefreshToken(refresh_token)
                
                # if no exeption is raised its a valid refrsh token
            except jwt.ExpiredSignatureError:  
                return Response({'error':'Refresh token has expierd.'},status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({'error':'Invalid refresh token.'},status=status.HTTP_401_UNAUTHORIZED)
            
            decoded_payload = jwt.decode(refresh_token, key=settings.SECRET_KEY, algorithms=['HS256'])  
            
            user_id = decoded_payload.get('user_id')
            
            user = get_user_model().objects.get(id = user_id)
            
            new_refresh = RefreshToken.for_user(user)
            
            token = {
                    'refresh': str(new_refresh),
                    'access': str(new_refresh.access_token)
                }
            
            data = {
                    'token': token,
                }
            
            return Response(data,status=status.HTTP_200_OK)
        
        except get_user_model().DoesNotExist:
            return Response({'error':'User assosiated with this token does not exist.'},status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error':f'error:{e}'},status=status.HTTP_400_BAD_REQUEST)
            
            
  
            
        
            
        

                        