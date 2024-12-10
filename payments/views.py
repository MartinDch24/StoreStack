from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import PaymentMethod
from .forms import PaymentMethodForm, PaymentMethodEditForm, PaymentMethodDeleteForm


class PaymentMethodCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = PaymentMethod
    form_class = PaymentMethodForm
    template_name = 'payments/payment-add.html'
    success_url = reverse_lazy('payments-detail')
    permission_required = 'payments.add_paymentmethod'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PaymentMethodsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = PaymentMethod
    template_name = 'payments/payments-detail.html'
    context_object_name = 'payment_methods'
    permission_required = 'payments.view_paymentmethod'

    def get_queryset(self):
        return PaymentMethod.objects.filter(user=self.request.user)


class PaymentMethodEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = PaymentMethod
    form_class = PaymentMethodEditForm
    template_name = 'payments/payment-edit.html'
    success_url = reverse_lazy('payments-detail')
    permission_required = 'payments.change_paymentmethod'

    def dispatch(self, request, *args, **kwargs):
        payment = self.get_object()

        if payment.user != self.request.user:
            return redirect('payments-detail')

        return super().dispatch(request, *args, **kwargs)


class PaymentMethodDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = PaymentMethod
    template_name = 'payments/payment-delete.html'
    success_url = reverse_lazy('payments-detail')
    form_class = PaymentMethodDeleteForm
    permission_required = 'payments.delete_paymentmethod'

    def get_initial(self):
        return self.get_object().__dict__

    def dispatch(self, request, *args, **kwargs):
        payment = self.get_object()

        if payment.user != self.request.user:
            return redirect('payments-detail')

        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        return super().form_valid(form)
