from rest_framework import status, viewsets, filters # for search filter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.generics import ListAPIView
from django_filters import rest_framework
from django.db.models import Avg, Min, Max,Sum, Count
from rest_framework_simplejwt.authentication import JWTAuthentication
from home import serializers
from home import models


class StoreView(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated,]
    filter_backends = [rest_framework.DjangoFilterBackend]
    filterset_fields = ['category']
    serializer_class = serializers.StoreSerializer
    queryset = models.Store.objects.all()
        
            
class ProductView(GenericViewSet,ListModelMixin,RetrieveModelMixin,):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated,]
    queryset = models.Product.objects.select_related('brand').all()
    
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category','brand','store']
    search_fields = ['^name']
    ordering_fields = ['name', 'price'] 
    ordering = ['id'] 
        
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.ProductDetailsSerializer
        else:
            return serializers.ProductSerializer
    
    def get_serializer_context(self):
        return {'query_set1': models.Wishlist.objects.filter(user=self.request.user).values_list('product', flat=True),
                'query_set2':{item['product']: item['avg'] 
                              for item in (models.Review.objects.select_related('product').values('product').annotate(avg=Avg("rate")))}}
    

class WishlistView(ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated,]
    serializer_class = serializers.WishlistSerializer
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddtoWishlistserializer
        return serializers.WishlistSerializer
    
    def get_queryset(self):
        user = self.request.user
        return models.Wishlist.objects.select_related('product').filter(user=user )
    
    
class ReviewView(ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated,]
    serializer_class = serializers.Reviewserializer
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddReviewSerializer
        return serializers.Reviewserializer
    
    def get_queryset(self):
        user = self.request.user
        return models.Review.objects.select_related('user','product').filter(user=user )