from django import forms
from django.forms import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class StoreStackUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError("The two password fields must match.")
        return password2


class StoreStackUserChangeForm(UserChangeForm):
    password1 = forms.CharField(label="New password", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Confirm new password", widget=forms.PasswordInput, required=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise ValidationError("The two password fields must match.")
        return password2

    def clean_password(self):
        password = self.cleaned_data.get('password1') or self.cleaned_data.get('password')

        if password:
            self.instance.set_password(password)
        return password
