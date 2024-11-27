from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.choices import UserType


class UserRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=UserType.choices,
        label="User Type",
        help_text="Select your account type."
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
    )


from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label="First Name")
    last_name = forms.CharField(max_length=30, required=False, label="Last Name")
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = Profile
        fields = ('bio', 'profile_picture', 'address_line_1', 'city', 'postal_code', 'country')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']

            if commit:
                self.user.save()
        if commit:
            profile.save()
        return profile
