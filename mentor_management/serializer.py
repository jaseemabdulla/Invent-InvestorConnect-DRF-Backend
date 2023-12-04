from rest_framework import serializers
from accounts.models import MentorProfile,BaseUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = '__all__'

class MentorProfileGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = MentorProfile
        fields = '__all__'
        

class MentorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorProfile
        fields = '__all__'        