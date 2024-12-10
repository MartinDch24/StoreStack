from cloudinary.models import CloudinaryField
import cloudinary
from cloudinary.exceptions import Error as ApiError
from django.contrib.auth import get_user_model
from django.db import models
from StoreStack.utils import product_image_folder


UserModel = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    image = CloudinaryField('image', folder=product_image_folder, blank=True, null=True)
    seller = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.image:
            public_ids = [f"{self.image}"]
            try:
                cloudinary.api.delete_resources(public_ids, resource_type="image", type="upload")
                cloudinary.api.delete_folder(product_image_folder(self))
            except ApiError as e:
                print(f"Error deleting Cloudinary resources: {e}")
        return super().delete(*args, **kwargs)
