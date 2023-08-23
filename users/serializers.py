from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from users import models
from cart.models import Cart


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        
        return token


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ['address',]


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id','name']


class UserSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=True,max_length=50)
    
    class Meta:
        model = models.User
        fields = ['email', 'name', 'password', 'address']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style':{'input_type': 'password'}
            }
        }
        
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            address = validated_data['address'],
            password = validated_data['password'])     
        models.Address.objects.create(user= user,address = user.address)
        Cart.objects.create(user= user)
        return user
    
    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
 
        return super().update(instance, validated_data)