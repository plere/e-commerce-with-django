from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    objects = UserManager()

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        primary_key = True,
        max_length = 150,
        unique = True,
        help_text = _('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators = [username_validator],
        error_messages = {
            'unique': _("A user with that username already exists."),
        },
    )
    address = models.CharField(max_length = 255, blank = True)
    phone_number = models.CharField(max_length = 13, blank = True)
