from django import forms

from orders.choices import StatusChoices
from orders.models import Order
from payments.models import PaymentMethod


class CheckoutForm(forms.Form):
    payment_method = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            payment_methods = PaymentMethod.objects.filter(user=user)
            if payment_methods.exists():
                self.fields['payment_method'].choices = [
                    (pm.id, f"{pm.card_type} ending in {pm.card_number[-4:]}") for pm in payment_methods
                ]
            else:
                self.fields['payment_method'].choices = [('', 'No Payment Methods available')]


class OrderStatusEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['status'].choices = (
            ('paid', 'Paid'),
            ('shipped', 'Shipped'),
            ('canceled', 'Canceled'),
            ('out_for_delivery', 'Out For Delivery'),
            ('completed', 'Completed'),
        )
