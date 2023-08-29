from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
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
        fields = ['id','address','address_status']


class AddAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ['address',]
        
    def create(self, validated_data):
            user_id = self.context['user_id']
            address = validated_data["address"]
            return models.Address.objects.create(user_id=user_id, address = address)


class UpdateAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ['address_status',]
      
    def update(self, instance, validated_data):
        user_id = self.context['user_id']
        if instance.address_status == False:
            current = models.Address.objects.select_related('user').get(user_id=user_id, address_status=True)
            current.address_status = False
            instance.address_status = True
            current.save()
        else:
            raise serializers.ValidationError('Please Choose Another Default')

        return super().update(instance, validated_data)


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
        models.Address.objects.create(user= user,address = user.address, address_status=True)
        Cart.objects.create(user= user)
        return user
    
    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
 
        return super().update(instance, validated_data)