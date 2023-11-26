from rest_framework import serializers
from .models import BaseUser,EntrepreneurProfile,InvestorProfile

class LoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField()
      
    
class SignupSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ('id','email','first_name','last_name','password','phone_number','role','is_blocked')
            extra_kwargs = {
                'password':{'write_only':True}
            }
            
        def create(self, validated_data):
            password = validated_data.pop('password',None)
            instance = self.Meta.model(**validated_data)
            
            if password is not None:
                instance.set_password(password)

            instance.save()
            return instance         
        

class EntrepreneurSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrepreneurProfile
        fields = '__all__'
        depth = 2
        
        
        
class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorProfile
        fields = '__all__'  
        depth = 2      

            