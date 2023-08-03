from rest_framework import serializers
from cart import models
from home.models import Product
from home.serializers import Productserializer


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name','final_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False, read_only=True)
    sub_total = serializers.SerializerMethodField(method_name='total')

    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'quantity', 'sub_total']
    
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


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(min_value = 1)
    quantity = serializers.IntegerField(min_value = 1) 
    
    class Meta:
        model = models.CartItem
        fields = ['id', 'product_id', 'quantity']
        
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data["product_id"] # type: ignore
        quantity = self.validated_data['quantity'] # type: ignore
        cartItem = models.CartItem.objects.filter(product_id=product_id, cart_id=cart_id).first()
        
        #### PUT , Update cart item or item already exists before update it
        if self.instance is not None or cartItem is not None:
            print("inside conditon")
            cartItem.quantity = quantity # type: ignore
            cartItem.save() # type: ignore
            self.instance = cartItem
        else: # Create new cartiem
            self.instance = models.CartItem.objects.create(cart_id=cart_id, product_id=product_id, quantity=quantity)
                    
        return self.instance
    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['quantity']
