from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters # for search filter
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.generics import ListAPIView
from django_filters import rest_framework

from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from cart import serializers
from cart import models

class CartViewSet(CreateModelMixin, GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer

class CartItemViewSet(ModelViewSet):
    
    def get_queryset(self):
        return models.CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
    serializer_class = serializers.CartItemSerializer



