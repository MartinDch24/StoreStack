from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from accounts.models import Profile
from accounts.choices import UserType
import cloudinary
from cloudinary.exceptions import Error as ApiError


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


User = get_user_model()


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank if you don't want to change your password.",
    )
    password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank if you don't want to change your password.",
    )

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

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("The two password fields didn’t match.")
            validate_password(password1, self.user)
        return cleaned_data

    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.instance.pk:
            old_instance = Profile.objects.get(pk=self.instance.pk)
            if old_instance.profile_picture and old_instance.profile_picture != self.instance.profile_picture:
                try:
                    public_id = old_instance.profile_picture
                    cloudinary.api.delete_resources([public_id], resource_type="image", type="upload")
                except ApiError as e:
                    print(f"Error deleting Cloudinary resources: {e}")

        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']

            if self.cleaned_data['password1']:
                self.user.set_password(self.cleaned_data['password1'])
            if commit:
                self.user.save()

        if commit:
            profile.save()

        return profile
