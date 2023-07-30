from django.contrib import admin
from users import models
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "address") 
    list_filter = ("name", "email", "address")  


admin.site.register(models.User, UserAdmin)