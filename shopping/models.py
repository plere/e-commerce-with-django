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

