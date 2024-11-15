from django.db import models

from accounts.models import StoreStackUser


class Profile(models.Model):
    user = models.OneToOneField(
        StoreStackUser,
        on_delete=models.CASCADE,
    )
    profile_picture = models.ImageField(upload_to='media/profile-pictures')
    bio = models.TextField()
