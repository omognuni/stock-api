from django.contrib.auth import get_user_model

from core.models import Account, Holding, Invest

from django.conf import settings

import csv
import os


def load_csv():
    fhand = open(os.path.join(settings.DATA_ROOT, 'account_asset_info_set.csv'))
    reader = csv.reader(fhand)
    count = 0
    for row in reader:
        count += 1
        if count == 1:
            continue
        row = [line.strip() for line in row]
        name, bank_name, account_number, account_name, ISIN, holding_price, holding_number = row
        try:
            int(account_number)
            if not get_user_model().objects.filter(username=account_number).exists():
                user = get_user_model().objects.create_user(username=account_number, password='testpass', first_name=name)
            else:
                user = get_user_model().objects.get(username=account_number)
            account, created = Account.objects.get_or_create(user=user, bank_name=bank_name, account_name=account_name, account_number=account_number)
            holding, created = Holding.objects.update_or_create(ISIN=ISIN, defaults={'holding_price':int(holding_price)})
            invest = Invest.objects.create(account=account, holding=holding, holding_number=int(holding_number))
        except Exception as e:
            print('Error', e)
            continue
            
    fhand = open(os.path.join(settings.DATA_ROOT, 'account_basic_info_set.csv'))
    reader = csv.reader(fhand)
    count = 0
    for row in reader:
        count += 1
        if count == 1:
            continue
        row = [line.strip() for line in row]
        account_number, principal = row
        try:
            principal = int(principal)
            if not get_user_model().objects.filter(username=account_number).exists():
                user = get_user_model().objects.create_user(username=account_number, password='testpass')
            else:
                user = get_user_model().objects.get(username=account_number)
            account, created = Account.objects.get_or_create(user=user, account_number=account_number)
            account.principal = principal
            account.save()
        except Exception as e:
            print('Error', e)
            continue

    fhand = open(os.path.join(settings.DATA_ROOT, 'asset_group_info_set.csv'))
    reader = csv.reader(fhand)
    count = 0
    for row in reader:
        count += 1
        if count == 1:
            continue
        row = [line.strip() for line in row]
        holding_name, ISIN, holding_type = row
        holding = Holding.objects.update_or_create(ISIN=ISIN, defaults = {'holding_name': holding_name, 'holding_type': holding_type})
        