from django.contrib.auth import get_user_model
from django.db import models
from cloudinary.models import CloudinaryField


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
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
