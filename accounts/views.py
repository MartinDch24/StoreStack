from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, DeleteView

from accounts.forms import UserRegistrationForm, UserLoginForm, ProfileEditForm
from accounts.models import Profile


UserModel = get_user_model()


class UserRegistrationView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('dash')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm


class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = "accounts/profile-detail.html"
    model = Profile

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileEditView(LoginRequiredMixin, FormView):
    template_name = "accounts/profile-edit.html"
    form_class = ProfileEditForm
    success_url = reverse_lazy('profile-detail')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['instance'] = self.request.user.profile
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = UserModel
    template_name = 'accounts/profile-delete.html'
    success_url = reverse_lazy('dash')

    def get_object(self, queryset=None):
        return self.request.user
