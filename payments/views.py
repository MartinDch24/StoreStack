from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import PaymentMethod
from .forms import PaymentMethodForm, PaymentMethodEditForm, PaymentMethodDeleteForm


class PaymentMethodCreateView(LoginRequiredMixin, CreateView):
    model = PaymentMethod
    form_class = PaymentMethodForm
    template_name = 'payments/payment-add.html'
    success_url = reverse_lazy('payments-detail')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PaymentMethodsView(LoginRequiredMixin, ListView):
    model = PaymentMethod
    template_name = 'payments/payments-detail.html'
    context_object_name = 'payment_methods'

    def get_queryset(self):
        return PaymentMethod.objects.filter(user=self.request.user)


class PaymentMethodEditView(LoginRequiredMixin, UpdateView):
    model = PaymentMethod
    form_class = PaymentMethodEditForm
    template_name = 'payments/payment-edit.html'
    success_url = reverse_lazy('payments-detail')

    def dispatch(self, request, *args, **kwargs):
        payment = self.get_object()

        if payment.user != self.request.user:
            return redirect('payments-detail')

        return super().dispatch(request, *args, **kwargs)


class PaymentMethodDeleteView(LoginRequiredMixin, DeleteView):
    model = PaymentMethod
    template_name = 'payments/payment-delete.html'
    success_url = reverse_lazy('payments-detail')
    form_class = PaymentMethodDeleteForm

    def get_initial(self):
        return self.get_object().__dict__

    def dispatch(self, request, *args, **kwargs):
        payment = self.get_object()

        if payment.user != self.request.user:
            return redirect('payments-detail')

        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        return super().form_valid(form)
