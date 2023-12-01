from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsEntrepreneur,IsAdmin,IsInvestor
from accounts.models import EntrepreneurProfile
from .serializer import StartupDetailSerializer,StartupGetSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .models import StartupDetail
from rest_framework import generics


# Create your views here.


 # ============================== Entrepreneur ===============================
 
class CreateStartup(APIView):
    permission_classes = [IsAuthenticated, IsEntrepreneur]
    def post(self, request):
        user = request.user
        entrepreneur = EntrepreneurProfile.objects.filter(user = user).first()
        
        startup_name = request.data.get('startup_name')
        
        if StartupDetail.objects.filter(startup_name=startup_name, entrepreneurs=entrepreneur).exists():
            data = {
                'message':'startup already exist'
            }
            return Response(data,status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data['entrepreneurs'] = entrepreneur.id

        try:
            serialazer = StartupDetailSerializer(data=data)
            serialazer.is_valid(raise_exception=True)
            serialazer.save()
            data = {
                'startup':serialazer.data,
                'message':'startup created succesfully'
            }
            return Response(data,status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            
            return Response({'errors':e.detail},status=status.HTTP_400_BAD_REQUEST) 
        
        
class ListUserStartups(generics.ListAPIView):
    serializer_class = StartupGetSerializer
    permission_classes = [IsAuthenticated, IsEntrepreneur]  
    
    def get_queryset(self):
        user = self.request.user
        
        user_startups = StartupDetail.objects.filter(entrepreneurs__user=user)
        
        return user_startups      
        

# ============================== Admin ===============================
        
class ListPendingStartups(generics.ListAPIView):
    queryset = StartupDetail.objects.filter(approval_status = 'pending')
    serializer_class = StartupGetSerializer
    permission_classes = [IsAuthenticated,IsAdmin]
    
    
class ListApprovedStartups(generics.ListAPIView):
    queryset = StartupDetail.objects.filter(approval_status = 'approved')
    serializer_class = StartupGetSerializer
    permission_classes = [IsAuthenticated,IsAdmin]    
    
    
class ListRejectedStartups(generics.ListAPIView):
    queryset = StartupDetail.objects.filter(approval_status = 'rejected')
    serializer_class = StartupGetSerializer
    permission_classes = [IsAuthenticated,IsAdmin]
    
    
class GetSingleStartup(generics.RetrieveAPIView):
    queryset = StartupDetail.objects.all()
    serializer_class = StartupGetSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
    
# update the staus of startup 

class UpdateStartupStatus(generics.RetrieveUpdateAPIView):
    queryset = StartupDetail.objects.all()
    serializer_class = StartupGetSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status = request.data.get('approval_status')
        
        # validation for status
        
        if new_status not in dict(StartupDetail.APPROVAL_CHOICES).keys():
            return Response({'messege':'Invalid approvel status'},status=status.HTTP_400_BAD_REQUEST)
        
        instance.approval_status = new_status
        instance.save()
        
        serializer = self.get_serializer(instance)
        return Response({'startup':serializer.data,'message': 'Startup status updated successfully'}, status=status.HTTP_200_OK)
            
        
            
              
        
