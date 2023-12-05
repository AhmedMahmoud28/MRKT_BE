from django.db import models
from django_lifecycle import BEFORE_CREATE, BEFORE_UPDATE, hook

from users import models


class AddressMixin:
    @hook(BEFORE_UPDATE, when='address_status', was=False, has_changed=True)
    @hook(BEFORE_CREATE)
    def on_update(self):
            user_id = self.user.id  # type: ignore
            current = models.Address.objects.select_related("user").get(user_id=user_id, address_status=True) # type: ignore
            if self != current:
                current.address_status = False
                self.address_status = True
                current.save()