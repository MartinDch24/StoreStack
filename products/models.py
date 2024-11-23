from cloudinary.models import CloudinaryField
import cloudinary
from django.db import models
from StoreStack.utils import product_image_folder


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = CloudinaryField('image', folder=product_image_folder, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        public_ids = [f"{self.image}"]
        image_delete_result = cloudinary.api.delete_resources(public_ids, resource_type="image", type="upload")
        cloudinary.api.delete_folder(f"products/{self.name}")
        super().delete(*args, **kwargs)
