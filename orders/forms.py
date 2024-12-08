from django import forms
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
