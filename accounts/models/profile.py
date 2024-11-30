from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from cloudinary.models import CloudinaryField
import re


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='profile',
    )
    profile_picture = CloudinaryField('image', folder='profile-pictures', blank=True, null=True)
    bio = models.TextField(blank=True, null=True, max_length=500)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def clean(self):
        super().clean()

        if self.postal_code:
            self.postal_code = self.postal_code.strip()

        postal_code_regex = r'^[A-Za-z0-9][A-Za-z0-9\s\-]{3,9}$'
        if not re.match(postal_code_regex, self.postal_code):
            raise ValidationError({'postal_code': 'Invalid postal code format. Please enter a valid postal code.'})

    def __str__(self):
        return f"Profile of {self.user.username}"
