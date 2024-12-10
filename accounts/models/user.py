from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from accounts.choices import UserType


class StoreStackUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        null=True,
        blank=True,
    )

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
