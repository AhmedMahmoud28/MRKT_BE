from rest_framework import serializers
from home import models
from cart.serializers import SimpleProductSerializer
from django.db import transaction
from django.db.models.query import QuerySet


class Storeserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = ['name', 'image']


class Productserializer(serializers.ModelSerializer):
    is_fav = serializers.SerializerMethodField(method_name='fav')
    
    class Meta:
        model = models.Product
        fields = ['name', 'image', 'final_price', 'brand', 'is_fav']
    
    def to_representation(self, instance):
        represent = super(Productserializer, self).to_representation(instance)
        represent['brand'] = instance.brand.name
        return represent
        
    def fav(self, obj):
        Q = self.context['query_set'] 
        # print(Q)
        return obj.id in Q
       
    # def fav(self, obj):
    #     user = self.context['user_id'] 
    #     return models.Wishlist.objects.filter(user=user, product_id=obj.id).exists()
    #     return obj.id in Q

class Wishlistserializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='user_of_list')
    product = SimpleProductSerializer(many=False)
    
    class Meta:
        model = models.Wishlist
        fields = "__all__"
        
    def user_of_list(self, obj):
        return self.context['user_id']


class AddtoWishlistserializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Wishlist
        fields = ['product']
    
    def save(self, **kwargs):
        with transaction.atomic(): 
            user_id = self.context['user_id']
            product_added = self.validated_data["product"] # type: ignore
            self.instance = models.Wishlist.objects.select_related('product').filter(user_id=user_id, product__id=product_added.id).first()
    
            if self.instance is None:
                return models.Wishlist.objects.select_related('product').create(user_id=user_id, product=product_added)              
                
            elif self.instance is not None:
                return self.instance.delete()
                