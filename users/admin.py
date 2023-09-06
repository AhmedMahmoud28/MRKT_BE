from django.contrib import admin

from users import models

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "date")
    list_filter = (
        "name",
        "email",
    )


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "address",
    )
    list_filter = ("user",)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Address, AddressAdmin)
