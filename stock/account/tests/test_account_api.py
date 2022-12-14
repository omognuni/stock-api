import hashlib
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Account, Holding, Invest

from account.serializers import AccountSerializer, AccountDetailSerializer


ACCOUNT_URL = reverse('account:account-list')


def deposit_valid_url(account_id):
    return reverse('account:account-deposit-valid', args = [account_id])

def deposit_url(account_id):
    return reverse('account:account-deposit', args = [account_id])

def detail_url(account_id):
    return reverse('account:account-detail', args = [account_id])

def create_account(user, **params):
    defaults = {
        'account_number' : '1112222',
        'bank_name': 'test bank',
        'account_name': 'test account',
        'principal': 1000000,        
    }
    defaults.update(params)
    
    return Account.objects.create(user=user, **defaults)

def create_holding(**params):
    defaults = {
        'ISIN': 'KR1000',
        'holding_name': 'testname',
        'holding_type':'미국 주식',
        'holding_price': 10000,
    }
    defaults.update(params)
    
    return Holding.objects.create(**defaults)

def create_invest(account,holding, **params):

    defaults = {
        'account': account,
        'holding': holding,
        'holding_number': 1,
    }
    defaults.update(params)
    
    return Invest.objects.create(**defaults)

class PrivateAPITest(TestCase):
    '''인증한 사용자 테스트'''
    def setUp(self):
        username = 'testname'
        password = 'testpass'
        self.user = get_user_model().objects.create_user(username=username, password=password)
        
        self.client = APIClient()
        
        self.client.force_authenticate(self.user)
        
    
    def test_retrieve_account(self):
        '''계좌 정보 목록 가져오기 테스트'''
        account = create_account(user=self.user)
        holding1 = create_holding()
        holding2 = create_holding(ISIN='KR2000',holding_name='testname2')
        
        invest1 = create_invest(account=account, holding=holding1, holding_number=10)
        invest2 = create_invest(account=account, holding=holding2, holding_number=1)
        
        # 총 자산 계산 코드
        assets = invest1.holding_number * invest1.holding.holding_price + \
            invest2.holding_number * invest2.holding.holding_price
        
        res = self.client.get(ACCOUNT_URL)
        
        account = Account.objects.all()
        serializer = AccountSerializer(account, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        
        # 자산 확인
        self.assertEqual(res.data[0]['assets'], assets)
            
    def test_retrieve_account_details(self):
        '''계좌 상세 정보 가져오기 테스트'''
        account = create_account(user=self.user)
        holding1 = create_holding()
        holding2 = create_holding(ISIN='KR2000',holding_name='testname2')
        
        invest1 = create_invest(account=account, holding=holding1, holding_number=10)
        invest2 = create_invest(account=account, holding=holding2, holding_number=1)
        
        assets = invest1.holding_number * invest1.holding.holding_price + \
            invest2.holding_number * invest2.holding.holding_price
        
        total_earnings = assets - account.principal
        earnings_rate = total_earnings / account.principal * 100
        
        url = detail_url(account.id)
        res = self.client.get(url)
        serializer = AccountDetailSerializer(account)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.data['assets'], assets)
        self.assertEqual(res.data['total_earnings'], total_earnings )
        self.assertEqual(res.data['earnings_rate'], earnings_rate)
        
        
        
    def test_retrieve_other_user_account_fail(self):
        '''다른 유저의 account 정보 없는지 확인'''
        create_account(user=self.user)
        user2 = get_user_model().objects.create_user(username='testname2', password='testpass')
        create_account(user=user2, account_number='333333333')
        
        res = self.client.get(ACCOUNT_URL)
        
        accounts = Account.objects.filter(user=self.user)
        serializer = AccountSerializer(accounts, many=True)
        
        self.assertEqual(res.data, serializer.data)
      
    def test_valid_deposit_to_account(self):
        '''입금 요청 검증 및 업데이트'''
        account = create_account(user=self.user)        
        
        # phase 1
        payload_1 = {
            'account_number': account.account_number,
            'username': self.user.username,
            'transfer_amount': 1000
        }
        new_deposit = account.deposit + payload_1['transfer_amount']
        
        url = deposit_valid_url(account.id)
        res = self.client.post(url, payload_1)
        
        self.assertEqual(res.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(res.data['transfer_id'], account.id)
        
        # phase 2
        key = f'{account.account_number}{self.user.username}{payload_1["transfer_amount"]}'
        cache_key = hashlib.sha512(key.encode("utf-8")).hexdigest()
        
        payload_2 = {
            'signature': cache_key,
            'transfer_id': res.data['transfer_id']
        }
        
        url = deposit_url(account.id)
        res = self.client.post(url, payload_2)
        account.refresh_from_db()
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # 송금 완료 후 잔액 테스트
        self.assertEqual(account.deposit, new_deposit)
        self.assertTrue(res.data['status'])

        