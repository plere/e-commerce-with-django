from django.db import models

# Create your models here.
from common.models import User


class Store(models.Model):
    store_name = models.CharField(primary_key = True, max_length = 128)
    password = models.CharField(max_length = 128)
    description = models.TextField(blank = True)

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True


class Item(models.Model):
    item_name = models.CharField(max_length = 255)
    stock_count = models.PositiveIntegerField()
    item_order_count = models.PositiveIntegerField(default = 0)
    item_price = models.PositiveIntegerField()
    item_description = models.TextField(blank = True, null = True)
    store = models.ForeignKey(Store, on_delete = models.CASCADE)


class Order(models.Model):
    class ShippingStatus(models.TextChoices):
        ORDER_OK = 'ORDER_OK'
        SHIPPING_READY = 'SHIPPING_READY'
        SHIPPING_START = 'SHIPPING_START'
        SHIPPING_COMPLETE = 'SHIPPING_COMPLETE'

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    order_count = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add = True)
    shipping_status = models.CharField(choices = ShippingStatus.choices, default = ShippingStatus.ORDER_OK, max_length = 20)

