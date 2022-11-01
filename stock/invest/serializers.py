from rest_framework import serializers

from core.models import Invest


class InvestSerializer(serializers.ModelSerializer):
    ISIN = serializers.CharField(source='holding.ISIN', read_only=True)
    holding_name = serializers.CharField(source='holding.holding_name', read_only=True)
    holding_type = serializers.CharField(source='holding.holding_type', read_only=True)
    holding_price = serializers.CharField(source='holding.holding_price', read_only=True)
    
    class Meta:
        model = Invest
        fields = ['id', 'ISIN', 'holding_name', 'holding_type', 'holding_price']
        read_only_fields = fields
