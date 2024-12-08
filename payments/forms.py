from django import forms
from .models import PaymentMethod
from datetime import datetime


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['card_type', 'card_number', 'expiry_month', 'expiry_year', 'cvc']
        widgets = {
            'card_type': forms.TextInput(attrs={'placeholder': 'e.g., Visa or MasterCard'}),
            'card_number': forms.TextInput(attrs={'placeholder': 'Enter your card number'}),
            'expiry_month': forms.NumberInput(attrs={'placeholder': 'MM'}),
            'expiry_year': forms.NumberInput(attrs={'placeholder': 'YYYY'}),
            'cvc': forms.PasswordInput(attrs={'placeholder': 'CVC'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        expiry_month = cleaned_data.get('expiry_month')
        expiry_year = cleaned_data.get('expiry_year')

        if expiry_month and expiry_year:
            current_year = datetime.now().year
            current_month = datetime.now().month

            if expiry_year < current_year or (expiry_year == current_year and expiry_month < current_month):
                raise forms.ValidationError("The expiry date cannot be in the past.")

        return cleaned_data


class PaymentMethodEditForm(PaymentMethodForm):
    pass


class PaymentMethodDeleteForm(PaymentMethodForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['disabled'] = True
            field.widget.attrs['readonly'] = True
