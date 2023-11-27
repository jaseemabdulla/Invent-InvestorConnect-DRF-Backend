from rest_framework import serializers
from .models import StartupDetail
from accounts.serializer import EntrepreneurSerializer


class StartupDetailSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = StartupDetail
        fields = '__all__'
        
        
class StartupGetSerializer(serializers.ModelSerializer):
    
    entrepreneurs = EntrepreneurSerializer(many=True)  # Use the EntrepreneurProfileSerializer for the entrepreneurs field
    
    class Meta:
        model = StartupDetail
        fields = '__all__'        
        