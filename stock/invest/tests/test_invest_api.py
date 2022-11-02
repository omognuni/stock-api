from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Account, Holding, Invest

from invest.serializers import InvestSerializer


INVEST_URL = reverse('invest:invest-list')

def create_account(user, **params):
    defaults = {
        'account_number' : '1112222',
        'bank_name': 'test bank',
        'account_name': 'test account',
        'deposit': 10000,
        'principal': 1000000,        
    }
    defaults.update(params)

    return Account.objects.create(user=user, **defaults)

def create_holding():
    defaults = {
        'ISIN': 'KR100000000',
        'holding_name': 'testname',
        'holding_type':'미국 주식',
        'holding_price': 10000,
    }
    
    return Holding.objects.create(**defaults)

class PrivateAPITest(TestCase):
    
    def setUp(self):
        username = 'testname'
        password = 'testpass'
        self.user = get_user_model().objects.create_user(username=username, password=password)
        
        self.client = APIClient()
        
        self.client.force_authenticate(self.user)
        
    
    def test_retrieve_invest(self):
        '''보유 종목 조회 테스트'''
        account = create_account(self.user)
        holding = create_holding()
        holding_number = 10
        
        Invest.objects.create(account=account, holding=holding,
                                       holding_number = holding_number)        
        res = self.client.get(INVEST_URL)
        invests = Invest.objects.all()
        serializer = InvestSerializer(invests, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        
    def test_retrieve_other_user_invest_invalid(self):
        '''다른 유저 종목 정보 없는지 확인'''
        account = create_account(self.user)
        holding = create_holding()
        holding_number = 10
        
        Invest.objects.create(account=account, holding=holding,
                                       holding_number = holding_number)   
        
        user2 = get_user_model().objects.create_user(username='testuser2', password='testpass')
        account2 = create_account(user=user2, account_number='33333333')
        
        Invest.objects.create(account=account2, holding=holding,
                                       holding_number = holding_number)
        
        res = self.client.get(INVEST_URL)
        
        invests = Invest.objects.filter(account__user=self.user)
        serializer = InvestSerializer(invests, many=True)
        
        self.assertEqual(res.data, serializer.data)
  