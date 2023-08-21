from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters # for search filter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django_filters import rest_framework
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.authtoken.models import Token
from cart import serializers
from cart import models
from cart import permissions


class CartViewSet(GenericViewSet, RetrieveModelMixin, DestroyModelMixin, ListModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.ControllingCart, IsAuthenticated,)
    serializer_class = serializers.CartSerializer
    
    def get_queryset(self):
        return models.Cart.objects.prefetch_related('items').filter(user_id=self.request.user.id)  # type: ignore
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    # def create(self, request, *args, **kwargs):
    #     cart = models.Cart.objects.filter(user=self.request.user).first()
    #     if cart:
    #         return Response({
    #             "Message": "User's Cart Already Exists"
    #         }, status=400)
        
    #     return super().create(request, args, kwargs) 
        


class CartItemViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.ControllingCartItem, IsAuthenticated)
    
    def get_queryset(self):
        return models.CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])
            
    def get_serializer_context(self):
        return {'cart_id' : self.kwargs['cart_pk'],}
    
    def get_serializer_class(self):
        if (self.request.method == "POST" or self.request.method == "PUT"):
            return serializers.AddCartItemSerializer
        elif self.request.method == "PATCH":
            return serializers.UpdateCartItemSerializer
        
        return serializers.CartItemSerializer
        
# ___________________________________________________________________________________________________________________
class OrderViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # serializer_class = serializers.OrderSerializer
    # queryset = models.Order.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = serializers.CreateOrderSerializer(data=request.data, context = {'user_id': self.request.user.id, # type: ignore
                                                                                     'cart_id': self.request.user.cart.id})  # type: ignore
        serializer.is_valid(raise_exception=True)
        order = serializer.save() 
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data)
            
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateOrderSerializer
        return serializers.OrderSerializer
    
    # def get_serializer_context(self):
    #     return {'user_id': self.request.user.id}  # type: ignore
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff: # type: ignore
            return models.Order.objects.all()
        return models.Order.objects.filter(owner=user)