from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models


UserModel = get_user_model()


class PaymentMethod(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='payment_methods')
    card_type = models.CharField(max_length=20)
    card_number = models.CharField(max_length=16, validators=[MinLengthValidator(16)])
    expiry_month = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text="Enter a valid month (1-12)"
    )
    expiry_year = models.PositiveIntegerField(
        validators=[MinValueValidator(2000)],
        help_text="Enter a valid year (e.g., 2024)"
    )
    cvc = models.CharField(max_length=3)

    def formatted_expiry(self):
        return f"{self.expiry_month:02}/{self.expiry_year}"

    def __str__(self):
        return f"Payment Method for {self.user.username} - {self.card_type} ending in {self.card_number[-4:]}"
