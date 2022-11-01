from rest_framework import serializers

from core.models import Account, Invest


class AccountSerializer(serializers.ModelSerializer):
    assets = serializers.SerializerMethodField(method_name='get_assets')
    
    class Meta:
        model = Account
        fields = ['id', 'account_name','bank_name','account_number', 'assets']
        read_only_fields = fields
        
    def get_assets(self, obj):
        '''총 자산 계산'''
        invests = Invest.objects.filter(account=obj.id)
    
        if invests.exists():
            assets = 0
            for invest in invests:
                assets += invest.holding_number * invest.holding.holding_price
            
            return assets
        return obj.principal
    
    
class AccountDetailSerializer(AccountSerializer):
    total_earnings = serializers.SerializerMethodField(method_name='get_total_earnings')
    earnings_rate = serializers.SerializerMethodField(method_name='earnings_rate')
    
    class Meta(AccountSerializer.Meta):
        fields = AccountSerializer.Meta.fields + ['principal', 'total_earnings', 'earnings_rate']
        
    def get_total_earnings(self, obj):
        pass
    def get_earnings_rate(self, obj):
        pass        
    