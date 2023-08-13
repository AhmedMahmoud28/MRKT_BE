from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters # for search filter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import ListAPIView
from django_filters import rest_framework

from home import serializers
from home import models
from home import permissions

class storeview(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated,]
    serializer_class = serializers.Storeserializer
    queryset = models.Store.objects.all()
    filter_backends = [rest_framework.DjangoFilterBackend]
    filterset_fields = ['category']
    permission_classes = [IsAuthenticatedOrReadOnly,]
    
# class productfilter(rest_framework.FilterSet):
#     # category = django_filters.CharFilter(name='category__name')
#     # category = django_filters.ModelMultipleChoiceFilter(name='name', queryset=models.ProductCategory.objects.all(), lookup_type="eq")

#     class Meta:
#         model = models.Product
#         fields = ('name', 'price', 'category', 'brand', 'store')
    

    
class productview(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated,]
    serializer_class = serializers.Productserializer
    queryset = models.Product.objects.all()
    permission_classes = [IsAuthenticated,]
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filter_class = productfilter
    filterset_fields = ['category','brand','store']
    ### Specifying filter of single choice
    search_fields = ['^name']
    ### Specifying search fields with sign to indicate the type of exact search
    ordering_fields = ['name', 'price'] 
    ### Specifying ordering fields by default it uses all fields on serializer class
    ordering = ['name'] 
    ### Specifying a default ordering
    
    def get_serializer_context(self):
        return {'user_id': self.request.user}  # type: ignore

    

class WishlistView(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated,]
    serializer_class = serializers.Wishlistserializer
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddtoWishlistserializer
        return serializers.Wishlistserializer
        
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}  # type: ignore
    
    def get_queryset(self):
        user = self.request.user
        return models.Wishlist.objects.filter(user=user )