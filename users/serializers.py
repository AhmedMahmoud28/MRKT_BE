from rest_framework import serializers

from cart.models import Cart
from users import models

from .models import User


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = models.Address
        fields = "__all__"


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    address = serializers.CharField(required=True, max_length=50)

    class Meta:
        model = models.User
        fields = ["email", "name", "password", "address"]
        extra_kwargs = {"password": {"write_only": True, "style": {"input_type": "password"}}}

    def create(self, validated_data):
        user = User.objects.create_user(  # type: ignore
            email=validated_data["email"],
            name=validated_data["name"],
            address=validated_data["address"],
            password=validated_data["password"],
        )
        models.Address.objects.create(user=user, address=user.address, address_status=True)
        Cart.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        return super().update(instance, validated_data)
