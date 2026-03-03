from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','phone','role','responder_category','is_available']
    
    def create(self, validated_data):
        role=validated_data.get('role')
        responder_category=validated_data.get('responder_category')
        if role == 'responder' and not responder_category:
            raise serializers.ValidationError("Responder category is required for responders.")
        

        password = validated_data.pop('password', None)

        user=User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            role=validated_data.get('role'),
            responder_category=validated_data.get('responder_category'),
            is_available=validated_data.get('is_available')
        )
        return user
