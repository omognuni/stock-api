from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from core.models import Invest

from invest.serializers import InvestSerializer


class InvestViewSet(viewsets.ModelViewSet):
    
    serializer_class = InvestSerializer
    queryset = Invest.objects.all()

    def get_queryset(self):
        queryset = self.queryset.select_related('account')   \
                    .filter(account__user=self.request.user)
        
        return queryset