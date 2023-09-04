from rest_framework import permissions


class ControllingCart(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if len(view.kwargs) == 0 :  
                return True
            else:
                if view.kwargs['pk'] == str(request.user.cart.id):
                    return True
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user 
    
    
class ControllingCartItem(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.kwargs['cart_pk'] == str(request.user.cart.id):
                return True
        else:
            return False
