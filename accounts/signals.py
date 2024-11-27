from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def manage_user_profile(sender, instance: UserModel, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
