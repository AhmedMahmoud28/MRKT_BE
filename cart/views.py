from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters # for search filter
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.generics import ListAPIView
from django_filters import rest_framework
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from cart import serializers
from cart import models


class CartViewSet(CreateModelMixin, GenericViewSet, RetrieveModelMixin, DestroyModelMixin, ListModelMixin):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer


class CartItemViewSet(ModelViewSet):
    
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_queryset(self):
        return models.CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
        
    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'cart_id' : self.kwargs['cart_pk']
        }
    
    def get_serializer_class(self):
        if self.request.method == "POST" or self.request.method == "PUT":
            return serializers.AddCartItemSerializer
        elif self.request.method == "PATCH":
            return serializers.UpdateCartItemSerializer
        
        return serializers.CartItemSerializer


   