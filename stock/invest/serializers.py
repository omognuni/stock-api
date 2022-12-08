from rest_framework import serializers

from core.models import Invest


class InvestSerializer(serializers.ModelSerializer):
    ISIN = serializers.CharField(source='holding.ISIN', read_only=True)
    holding_name = serializers.CharField(source='holding.holding_name', read_only=True)
    holding_type = serializers.CharField(source='holding.holding_type', read_only=True)
    value = serializers.SerializerMethodField(method_name='get_value')
    
    class Meta:
        model = Invest
        fields = ['id', 'ISIN', 'holding_name', 'holding_type', 'value']
        read_only_fields = fields

   
    def get_value(self, obj):
        '''보유 종목 평가액'''
        value = obj.holding_number * obj.holding.holding_price
        return value