from django.db import models


# Create your models here.
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
