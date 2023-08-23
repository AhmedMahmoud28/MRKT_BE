from rest_framework import serializers
from django.db import transaction
from django.db.models import F
from cart import models
from home.serializers import SimpleProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False, read_only=True)
    sub_total = serializers.SerializerMethodField(method_name='total')

    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'quantity', 'sub_total']
    
    def total(self, cartitem:models.CartItem):
        return cartitem.quantity * cartitem.product.price
        
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only = True )
    total = serializers.SerializerMethodField(method_name='grand_total')

    class Meta:
        model = models.Cart
        fields = ['items','total']
        
    def grand_total(self, cart:models.Cart):
        items = cart.items.all()  # type: ignore
        total = sum(item.quantity * item.product.price for item in items)
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
        self.instance = models.CartItem.objects.filter(product_id=product_id, cart_id=cart_id).first()
        
        if self.instance is not None:
            self.instance.quantity = quantity 
            self.instance.save() 
        else: 
            self.instance = models.CartItem.objects.create(cart_id=cart_id, product_id=product_id, quantity=quantity)
                    
        return self.instance
    

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    sub_total = serializers.SerializerMethodField(method_name='total')
    
    class Meta:
        model = models.OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price', 'sub_total']

    def total(self, obj):
        return obj.quantity * obj.unit_price


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Order
        fields = ['id', 'date', 'pending_status', 'owner', 'items', 'total']
        

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.SerializerMethodField()
    
    def get_cart(self, obj):
        return self.context['cart_id']
    
    def save(self, **kwargs):
        with transaction.atomic(): 
            cart_id = self.context['cart_id']
            user_id = self.context['user_id']
            
            if not models.Cart.objects.filter(pk=cart_id).exists():
                raise serializers.ValidationError("this is invalid cart id")
            
            elif cart_id != models.Cart.objects.filter(user_id= user_id).values_list('id', flat=True)[0] :
                raise serializers.ValidationError("you don't have permission for this action")
            
            elif not models.CartItem.objects.filter(cart_id=cart_id).exists():
                raise serializers.ValidationError("sorry it's empty")
            
            cartitems = models.CartItem.objects.filter(cart_id = cart_id)
            total = sum(item.product.price * item.quantity for item in cartitems)
            order  = models.Order.objects.create(owner_id = user_id, total= total)
            orderitems = [models.OrderItem(order=order,
                                product=item.product,
                                quantity=item.quantity,
                                unit_price=item.product.price)
            for item in cartitems
            ]
            models.OrderItem.objects.bulk_create(orderitems)
            for item in orderitems:
                Q = models.Product.objects.values_list('id', flat=True)
                for i in Q:
                    if item.product.id == i: # type: ignore
                        models.Product.objects.filter(id= i).update(inventory= F('inventory') - item.quantity)
            models.CartItem.objects.filter(cart_id=cart_id).delete()
            return order