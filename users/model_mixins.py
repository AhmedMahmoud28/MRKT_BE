from django_lifecycle import AFTER_CREATE, BEFORE_CREATE, BEFORE_UPDATE, hook


class AddressMixin:
    @hook(BEFORE_UPDATE, when="address_status", was=False, has_changed=True)
    @hook(BEFORE_CREATE)
    def on_update(self):
        from .models import Address

        user_id = self.user.id  # type: ignore
        if (
            Address.objects.select_related("user")
            .filter(user_id=user_id, address_status=True)
            .exists()
        ):
            current = Address.objects.select_related("user").get(user_id=user_id, address_status=True)  # type: ignore
            if self != current:
                current.address_status = False
                self.address_status = True
                current.save()


class UserMixin:
    @hook(AFTER_CREATE)
    def on_creation(self):
        from cart.models import Cart

        Cart.objects.create(user=self)
