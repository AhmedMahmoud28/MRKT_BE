from rest_framework import serializers
from cart import models
from home.models import Product
from home.serializers import Productserializer

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','final_price']

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False, read_only=True)
    sub_total = serializers.SerializerMethodField(method_name='total')
    class Meta:
        model = models.CartItem
        fields = ['id','product', 'quantity', 'sub_total']
    
    def total(self, cartitem:models.CartItem):
        return cartitem.quantity * cartitem.product.final_price
    
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    items = CartItemSerializer(many=True, read_only = True )
    total = serializers.SerializerMethodField(method_name='grand_total')
    class Meta:
        model = models.Cart
        fields = ['id', 'items','total']
        
    def grand_total(self, cart:models.Cart):
        items = cart.items.all() # type: ignore
        total = sum(item.quantity * item.product.final_price for item in items)
        return total

