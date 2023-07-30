from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    
    def create_user(self, email, name, address, password=None):
        if not email:
            raise ValueError('User must have an email')
        
        email = self.normalize_email(email)
        user = self.model(email= email, name=name, address=address)
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, address, password=None):
        user = self.create_user(email, name,address, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
        
            

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    # address = models.ForeignKey("Address", on_delete=models.CASCADE)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','address']
    
    def __str__(self):
        return f"{self.name} {self.email}"
    











































# class User(models.Model):
#     name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=254)
#     password = models.CharField(max_length=50)
#     address = models.ForeignKey("Address", on_delete=models.CASCADE)
    
# class Address(models.Model): 
#     addresses = models.CharField(max_length=50)