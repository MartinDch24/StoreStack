from django import forms
from products.models import Product


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }
