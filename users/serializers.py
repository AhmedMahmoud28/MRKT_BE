from rest_framework import serializers
from .models import User
from users import models

class userserializer(serializers.ModelSerializer):
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
        return user
    
    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
 
        return super().update(instance, validated_data)