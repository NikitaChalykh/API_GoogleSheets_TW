from rest_framework import serializers

from orders.models import GoodsOrder


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsOrder
        fields = (
            'serial_number',
            'order_number',
            'dollar_value',
            'rub_value',
            'delivery_date'
        )


class TotalSerializer(serializers.Serializer):
    total_dollars = serializers.IntegerField()
    total_rubles = serializers.FloatField()
