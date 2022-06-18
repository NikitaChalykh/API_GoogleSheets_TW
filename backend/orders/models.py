from django.db import models


class GoodsOrder(models.Model):
    '''Модель заказов'''
    serial_number = models.PositiveSmallIntegerField(
        verbose_name='Порядковый номер'
    )
    order_number = models.PositiveIntegerField(
        verbose_name='Номер заказа'
    )
    dollar_value = models.PositiveIntegerField(
        verbose_name='Стоимость в долларах'
    )
    rub_value = models.FloatField(
        verbose_name='Стоимость в рублях'
    )
    delivery_date = models.DateField(
        verbose_name='Срок поставки'
    )
    is_sending = models.BooleanField(
        default=False,
        verbose_name='Статус отправки в телеграмм'
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['serial_number']

    def __str__(self):
        return str(self.order_number)
