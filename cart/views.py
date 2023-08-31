from rest_framework.response import Response
from rest_framework import status, viewsets, filters 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication
from cart import serializers
from cart import models
from cart import permissions


class CartViewSet(GenericViewSet, RetrieveModelMixin, DestroyModelMixin, ListModelMixin):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.ControllingCart, IsAuthenticated,)
    serializer_class = serializers.CartSerializer
    pagination_class = None
    
    def get_queryset(self):
        return models.Cart.objects.select_related('user').prefetch_related('items', 'items__product').filter(user_id=self.request.user.id)  # type: ignore
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        models.CartItem.objects.filter(cart=instance).delete()
       
   
class CartItemViewSet(ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.ControllingCartItem, IsAuthenticated)
    pagination_class = None

    def get_queryset(self):
        return models.CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])
    
    def get_serializer_context(self):
        context = {'cart_id': self.request.user.cart.id} # type: ignore
        return context
    
    def get_serializer_class(self):
        if (self.request.method == "POST" or self.request.method == "PUT"):
            return serializers.AddCartItemSerializer
        elif self.request.method == "PATCH":
            return serializers.UpdateCartItemSerializer
        
        return serializers.CartItemSerializer

   
class OrderViewSet(ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    
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
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff: # type: ignore
            return models.Order.objects.prefetch_related('items', 'items__product').all()
        return models.Order.objects.prefetch_related('items', 'items__product').filter(owner=user)