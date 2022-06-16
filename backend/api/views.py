from django.db.models import Sum
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import GoodsOrder

from .serializers import OrderSerializer, TotalSerializer


class OrdersViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = GoodsOrder.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'serial_number'

    @action(
        detail=False,
        methods=['GET'],
    )
    def total(self, request):
        dollar_sum = self.queryset.aggregate(
            Sum('dollar_value')
        )['dollar_value__sum']
        rub_sum = self.queryset.aggregate(
            Sum('rub_value')
        )['rub_value__sum']
        serializer = TotalSerializer(
            {'total_dollars': dollar_sum, 'total_rubles': rub_sum}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
