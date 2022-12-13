from django.contrib.auth import get_user_model

from core.models import Account, Holding, Invest

from django.conf import settings

import csv
import os


def load_csv():
    account_asset_info = open(os.path.join(settings.DATA_ROOT, 'account_asset_info_set.csv'), 'r+')
    account_asset_info_reader = csv.reader(account_asset_info)

    account_basic_info = open(os.path.join(settings.DATA_ROOT, 'account_basic_info_set.csv'))
    account_basic_info_reader = csv.reader(account_basic_info)
    
    asset_group_info = open(os.path.join(settings.DATA_ROOT, 'asset_group_info_set.csv'))
    asset_group_info_reader = csv.reader(asset_group_info)
    
    # csv 첫번째 줄(column 이름) 스킵
    next(account_asset_info_reader)
    next(account_basic_info_reader)
    next(asset_group_info_reader)
    
    # 유저 생성 및 계좌, 보유 종목 업데이트
    for row in account_asset_info_reader:
        row = [line.strip() for line in row]
        name, bank_name, account_number, account_name, ISIN, holding_price, holding_number = row
        try:
            if not get_user_model().objects.filter(username=account_number).exists():
                user = get_user_model().objects.create_user(username=account_number, password='testpass', first_name=name)
            else:
                user = get_user_model().objects.get(username=account_number)
            account, _ = Account.objects.update_or_create(user=user, bank_name=bank_name, account_name=account_name, account_number=account_number)
            holding, _ = Holding.objects.update_or_create(ISIN=ISIN, defaults={'holding_price':int(holding_price)})
            Invest.objects.create(account=account, holding=holding, holding_number=int(holding_number))
        except Exception as e:
            print('Error', e)
            continue
    
    for row in account_basic_info_reader:
        row = [line.strip() for line in row]
        account_number, principal = row
        try:
            principal = int(principal)
            if not get_user_model().objects.filter(username=account_number).exists():
                user = get_user_model().objects.create_user(username=account_number, password='testpass')
            else:
                user = get_user_model().objects.get(username=account_number)
            account, _ = Account.objects.get_or_create(user=user, account_number=account_number)
            account.principal = principal
            account.save()
        except Exception as e:
            print('Error', e)
            continue
    
    # 주식 종목 정보 업데이트
    for row in asset_group_info_reader:
        row = [line.strip() for line in row]
        holding_name, ISIN, holding_type = row
        holding = Holding.objects.update_or_create(ISIN=ISIN, defaults = {'holding_name': holding_name, 'holding_type': holding_type})
    
    account_asset_info.close()
    account_basic_info.close()  
    asset_group_info.close()