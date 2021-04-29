from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    objects = UserManager()

    address = models.CharField(max_length = 255, blank = True)
    phone_number = models.CharField(max_length = 13, blank = True)
