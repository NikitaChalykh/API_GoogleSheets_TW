from django.contrib import admin

from .models import GoodsOrder


class GoodsOrderAdmin(admin.ModelAdmin):
    list_display = (
        'serial_number',
        'order_number',
        'dollar_value',
        'rub_value',
        'delivery_date',
        'is_sending'
    )


admin.site.register(GoodsOrder, GoodsOrderAdmin)
