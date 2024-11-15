from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.choices import UserType


class StoreStackUser(AbstractUser):
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.BUYER
    )

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
