from cloudinary import CloudinaryResource
from django import forms
from django.core.exceptions import ValidationError

from products.models import Product


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if isinstance(image, CloudinaryResource):
            return image
        elif image:
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                raise ValidationError("The image must be a valid image format (JPEG, PNG, GIF or WEBP).")
        else:
            return None
        return image


class ProductEditForm(ProductCreateForm):
    pass
