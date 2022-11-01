from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Account, Invest, Holding

def create_user():
    return get_user_model().objects.create_user(username='testname', password='testpass')

def create_account():
    user = create_user()
    defaults = {
        'account_number' : 1112222,
        'bank_name': 'test bank',
        'account_name': 'test account',
        'assets': 1000000,        
    }

    return Account.objects.create(user=user, **defaults)

def create_holding():
    defaults = {
        'ISIN': 'KR100000000',
        'holding_name': 'testname',
        'holding_type':'미국 주식',
        'holding_price': 10000,
    }
    
    return Holding.objects.create(**defaults)


class ModelTest(TestCase):
    '''모델 테스트'''
    
    def test_create_user_model(self):
        '''user model 생성 테스트'''
        username = 'testname'
        password = 'testpass'
        
        user = get_user_model().objects.create_user(username=username, password=password)
        
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        
    def test_create_account_model(self):
        '''Account model 생성 테스트'''
        user = create_user()
        account_number = 1112222
        bank_name = 'test bank'
        account_name = 'test account'
        assets = 1000000
        
        account = Account.objects.create(user=user, account_number=account_number, 
                                         bank_name=bank_name,account_name=account_name,
                                         assets=assets)
        
        self.assertEqual(str(account), account_name)
        self.assertEqual(account.user, user)
        
    def test_create_holding_model(self):
        '''Holding model 생성 테스트'''
        ISIN = 'KR100000000'
        holding_name = 'testname'
        holding_type = '미국 주식'
        holding_price = 10000
        
        holding = Holding.objects.create(ISIN=ISIN, holding_name=holding_name,
                                         holding_type=holding_type, holding_price=holding_price)
        
        self.assertEqual(str(holding), holding_name)
          
    def test_create_invest_model(self):
        '''Invest model 생성 테스트'''
        account = create_account()
        holding = create_holding()
        holding_number = 1
        
        invest = Invest.objects.create(account=account, holding=holding, holding_number=holding_number)
        
        self.assertEqual(invest.account, account)
        self.assertEqual(invest.holding, holding)
