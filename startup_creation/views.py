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
from rest_framework.pagination import PageNumberPagination


# Create your views here.


# for pagination

class ListAllStartupsPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100


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
    pagination_class = ListAllStartupsPagination
    
    def get_queryset(self):
        user = self.request.user
        
        user_startups = StartupDetail.objects.filter(entrepreneurs__user=user).order_by('-created_at')
        
        return user_startups 
     
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Calculate total pages based on count and items per page
        items_per_page = self.paginator.page_size
        total_items = response.data['count']
        total_pages = -(-total_items // items_per_page)  # Equivalent to ceil(total_items / items_per_page)

        # Add total pages and current page to the response data
        response.data['total_pages'] = total_pages
        response.data['current_page'] = self.paginator.page.number
        
        return response    

# list all startups 

class ListAllStartups(generics.ListAPIView):
    queryset = StartupDetail.objects.all().order_by('-created_at')
    serializer_class = StartupGetSerializer
    pagination_class = ListAllStartupsPagination
    
    def get_queryset(self):
        # Get the 'startup_industry' query parameter from the request
        industry = self.request.query_params.get('startup_industry', None)

        # Filter the queryset based on the provided industry
        if industry == 'all':
            return self.queryset
        else:
            return self.queryset.filter(startup_industry=industry)
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Calculate total pages based on count and items per page
        items_per_page = self.paginator.page_size
        total_items = response.data['count']
        total_pages = -(-total_items // items_per_page)  # Equivalent to ceil(total_items / items_per_page)

        # Add total pages and current page to the response data
        response.data['total_pages'] = total_pages
        response.data['current_page'] = self.paginator.page.number
        
        return response
  
# startup's IndustryChoices 
    
class IndustryChoicesView(APIView):
    def get(self, request, *args, **kwargs):
        industry_choices = [choice for choice in StartupDetail.INDUSTRY_CHOICES]
        return Response({'industry_choices': industry_choices})
    
        

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
    permission_classes = [IsAuthenticated]
    
    
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
            
        
            
              
        
