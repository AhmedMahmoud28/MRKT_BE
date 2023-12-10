class CurrentCartDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["request"].user.cart

    def __repr__(self):
        return "%s()" % self.__class__.__name__
