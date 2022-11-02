import hashlib

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth import get_user_model
from django.core.cache import cache

from core.models import Account

from account.serializers import AccountSerializer, AccountDetailSerializer


class AccountViewSet(viewsets.ModelViewSet):
    
    serializer_class = AccountDetailSerializer
    queryset = Account.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        
        return queryset
    
    def get_serializer_class(self):
        '''action에 따라 serializer 변경'''
        if self.action == 'list':
            return AccountSerializer
        return self.serializer_class
    
    @action(methods=['POST'], detail=True, url_path='deposit-valid')
    def deposit_valid(self, request, pk=None):
        '''계좌 송금 검증'''
        account = self.get_object()
        transfer_amount = request.data['transfer_amount']
        if account.account_number == request.data['account_number']:
            key = f'{account.account_number}{request.user.username}{transfer_amount}'
            cache_key = hashlib.sha512(key.encode("utf-8")).hexdigest() + f':{transfer_amount}'
            cache.set(pk, cache_key, 60)
            return Response({'transfer_id': int(pk)}, status=status.HTTP_202_ACCEPTED)
        
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    
    @action(methods=['POST'], detail=True, url_path='deposit')
    def deposit(self, request, pk=None):
        '''계좌 송금 완료'''
        account_id = request.data['transfer_id']
        cache_key, transfer_amount = cache.get(account_id).split(':')
        account = Account.objects.get(id=account_id)
        if request.data["signature"] == cache_key:
            account.deposit += int(transfer_amount)
            account.save()
            return Response({'status': True}, status.HTTP_200_OK)
        return Response({'status': False}, status=status.HTTP_400_BAD_REQUEST)
    
            
            
                        


