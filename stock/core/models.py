from django.db import models
from django.conf import settings


class Account(models.Model):
    '''이용자 계좌 모델'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=30, unique=True)
    account_name = models.CharField(max_length=255, blank=True)
    bank_name = models.CharField(max_length=255, blank=True)
    deposit = models.IntegerField(blank=True, default=0)
    principal = models.IntegerField(blank=True, default=0)
 
    def __str__(self):
        return self.account_number


class Holding(models.Model):
    '''주식 종목 모델'''
    ISIN = models.CharField(max_length=1024, unique=True)
    holding_name = models.CharField(max_length=255)
    holding_type = models.CharField(max_length=255)
    holding_price = models.IntegerField(blank=True, default=0)
        
    def __str__(self):
        return self.holding_name


class Invest(models.Model):
    '''투자 종목 모델'''
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    holding = models.ForeignKey('Holding', on_delete=models.SET_NULL, null=True)
    holding_number = models.IntegerField(default=0)
        