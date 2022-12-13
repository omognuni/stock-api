from rest_framework import serializers

from django.db.models import Sum, F

from core.models import Account, Invest


class AccountSerializer(serializers.ModelSerializer):
    assets = serializers.SerializerMethodField(method_name='get_assets', read_only=True)
    
    class Meta:
        model = Account
        fields = ['id', 'account_name','bank_name','account_number', 'assets']
        read_only_fields = ['id', 'account_name','bank_name','account_number','principal', 'assets']
        
    def get_assets(self, obj):
        '''총 자산 계산'''
        assets = Invest.objects.filter(account=obj.id). \
            aggregate(assets=Sum(F('holding_number')*F('holding__holding_price')))
        if assets['assets']:
            return assets['assets']
        
        return obj.principal

    
    
class AccountDetailSerializer(AccountSerializer):
    total_earnings = serializers.SerializerMethodField(method_name='get_total_earnings', read_only=True)
    earnings_rate = serializers.SerializerMethodField(method_name='get_earnings_rate', read_only=True)
    
    class Meta(AccountSerializer.Meta):
        fields = AccountSerializer.Meta.fields + ['principal', 'total_earnings', 'earnings_rate']
        
    def get_total_earnings(self, obj):
        '''총 수익금 계산'''
        total_earnings = self.get_assets(obj) - obj.principal
        return total_earnings
    
    def get_earnings_rate(self, obj):
        '''수익률 계산'''
        earnings_rate = 'principal must be set'
        if obj.principal:
            earnings_rate = self.get_total_earnings(obj) / obj.principal * 100
        return earnings_rate
    