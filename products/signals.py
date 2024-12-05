import cloudinary
from cloudinary.exceptions import Error as ApiError
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from products.models import Product


@receiver(pre_delete, sender=Product)
def delete_profile_picture(sender, instance, **kwargs):
    if instance.image:
        try:
            public_ids = [f"{instance.image}"]
            cloudinary.api.delete_resources(public_ids, resource_type="image", type="upload")
            cloudinary.api.delete_folder(f"products/{instance.name}")
        except ApiError as e:
            print(f"Error deleting Cloudinary resources: {e}")
