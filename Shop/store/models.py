from django.db import models

class Shop(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя магазина")
    open = models.BooleanField(default=True, verbose_name="Открыт")

class Order(models.Model):
    STATUS_CHOICES = [
        ('preparing', 'Готовится'),
        ('delivering', 'Доставка'),
        ('completed', 'Завершен')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='preparing', verbose_name="Статус")
    amount = models.IntegerField(verbose_name="Сумма")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="Магазин")
