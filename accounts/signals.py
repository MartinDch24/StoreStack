from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from accounts.models import Profile
import cloudinary
from cloudinary.exceptions import Error as ApiError

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def manage_user_profile(sender, instance: UserModel, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


@receiver(pre_delete, sender=Profile)
def delete_profile_picture(sender, instance, **kwargs):
    if instance.profile_picture:
        try:
            public_ids = [f"{instance.profile_picture}"]
            cloudinary.api.delete_resources(public_ids, resource_type="image", type="upload")
        except ApiError as e:
            print(f"Error deleting Cloudinary resources: {e}")


@receiver(post_save, sender=UserModel)
def assign_is_superuser_to_moderator(sender, instance, created, **kwargs):
    if created:
        if instance.groups.filter(name='Admin').exists():
            instance.is_superuser = True
            instance.save()


@receiver(post_save, sender=UserModel)
def assign_group_based_on_user_type(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'moderator':
            group = Group.objects.get(name='Moderator')
        elif instance.user_type == 'seller':
            group = Group.objects.get(name='Seller')
        elif instance.user_type == 'buyer':
            group = Group.objects.get(name='Buyer')
        elif instance.user_type == 'admin':
            group = Group.objects.get(name='Admin')
        else:
            group = None

        if group:
            instance.groups.add(group)
            if instance.user_type in ['moderator', 'admin']:
                instance.is_staff = True
        instance.save()
