from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.conf import settings
#from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save

# Create your models here.
cointype = (
    ('BTC','BTC'),
    ('ETH','ETH'),

)

# class EnrollUser(models.Model):
#     email = models.EmailField()
#     username = models.CharField(max_length=1000)
#     mobno = models.BigIntegerField()


class MyUser(AbstractUser):
    username = models.CharField(max_length=1000, unique=True)
    email = models.EmailField(max_length=255)
    mobno = models.BigIntegerField(unique=True)



    USERNAME_FIELD = 'mobno'
    REQUIRED_FIELDS = ['username','email']

    def __str__(self):
        return self.email


class Notification(models.Model):
    us = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    coin = models.CharField(max_length=100,choices=cointype,default='BTC')
    coinprice = models.BigIntegerField()

    class Meta:
        verbose_name_plural = "Tracking Notifications!"