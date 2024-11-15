from django.db import models


class UserType(models.TextChoices):
    BUYER = "buyer", "Buyer"
    SELLER = "seller", "Seller"
    ADMIN = "admin", "Admin"
