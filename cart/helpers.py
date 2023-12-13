class CurrentCartDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["request"].user.cart

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class CurrentAddressDefault:
    requires_context = True

    def __call__(self, serializer_field):
        from django.shortcuts import get_object_or_404

        from users.models import Address

        user = serializer_field.context["request"].user
        address = get_object_or_404(Address, user=user, address_status=True)

        return address

    def __repr__(self):
        return "%s()" % self.__class__.__name__
