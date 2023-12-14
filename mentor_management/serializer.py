from rest_framework import serializers
from accounts.models import MentorProfile,BaseUser
from .models import MentorRequest
from accounts.serializer import EntrepreneurSerializer
from startup_creation.serializer import StartupGetSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = '__all__'

class MentorProfileGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    entrepreneurs_count = serializers.SerializerMethodField()
    class Meta:
        model = MentorProfile
        fields = '__all__'
        
    def get_entrepreneurs_count(self, obj):
        return obj.entrepreneurs.count()      

class MentorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorProfile
        fields = '__all__'    
        
        
class MentorRequestSerializer(serializers.ModelSerializer):
    entrepreneur = EntrepreneurSerializer()
    startup_details = StartupGetSerializer(source='entrepreneur.startups', many=True, read_only=True)
    class Meta:
        model = MentorRequest
        fields = '__all__' 