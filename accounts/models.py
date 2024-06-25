from django.db import models
from django.contrib.auth.models import User
from book.models import Book

class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='address', on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, blank=True, null=True)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100,blank = True, null = True)
    postal_code = models.CharField(max_length=20)
    def __str__(self):
        return str(self.user.email)

class UserBankAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)