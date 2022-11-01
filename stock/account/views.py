from rest_framework import viewsets

from django.contrib.auth import get_user_model

from core.models import Account

from account.serializers import AccountSerializer, AccountDetailSerializer


class AccountViewSet(viewsets.ModelViewSet):
    
    serializer_class = AccountDetailSerializer
    queryset = Account.objects.all()
    
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        
        return queryset
    
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return AccountSerializer
        return self.serializer_class


