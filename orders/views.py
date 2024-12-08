from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework import request

from payments.models import PaymentMethod
from products.models import Product
from .forms import CheckoutForm
from .models import Order, OrderItem


class CartView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'orders/cart.html'
    permission_required = 'orders.view_orderitem'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order, created = Order.objects.get_or_create(user=self.request.user, status='pending')
        context['order'] = order
        return context


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return redirect('dash')

        if product.seller == request.user:
            return redirect('dash')

        order, created = Order.objects.get_or_create(user=request.user, status="pending")
        order_item = order.items.filter(product=product).first()

        if order_item and product.stock:
            if order_item.quantity < product.stock:
                order_item.quantity += 1
                order_item.save()
        elif product.stock:
            OrderItem.objects.create(order=order, product=product, quantity=1, price=product.price)
        return redirect('cart')


class RemoveFromCartView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'orders.delete_orderitem'

    def get(self, request, pk):
        order = Order.objects.filter(user=request.user, status='pending').first()

        if order:
            order_item = get_object_or_404(OrderItem, id=pk, order=order)
            order_item.delete()

        return redirect('cart')


class CheckoutView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'orders/checkout.html'
    permission_required = 'orders.add_order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_id = self.kwargs.get('product_id')

        if product_id:
            product = get_object_or_404(Product, id=product_id)
            context['products'] = [product]
            context['total_price'] = product.price
        else:
            order = Order.objects.filter(user=self.request.user, status="pending").first()
            if order:
                context['products'] = order.items.all()
                context['total_price'] = order.get_total_cost()
            else:
                return redirect('cart')

        context['form'] = CheckoutForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST, user=request.user)

        if not form.is_valid():
            return redirect('checkout')

        payment_method_id = form.cleaned_data['payment_method']
        payment_method = get_object_or_404(PaymentMethod, id=payment_method_id, user=request.user)

        order = Order.objects.filter(user=request.user, status='pending').first()

        if not order:
            return redirect('cart')

        if order.items.count() == 0:
            return redirect('cart')

        for item in order.items.all():
            if item.product.seller == request.user:
                item.delete()
                return redirect('checkout')

        order.status = 'paid'
        order.payment_method = payment_method
        order.save()

        return redirect('dash')


class MyOrdersView(LoginRequiredMixin, ListView):
    template_name = 'orders/my-orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user).exclude(status='pending').order_by('-updated_at')


class OrderedProductsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'orders/ordered-products.html'
    context_object_name = 'order_items'
    permission_required = 'products.add_product'

    def get_queryset(self):
        user = self.request.user
        return OrderItem.objects.filter(product__seller=user).exclude(order__status='pending').order_by('-order__updated_at')


class OrderStatusUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Order
    fields = ['status']
    template_name = 'orders/update-order-status.html'
    permission_required = 'products.add_product'
    success_url = reverse_lazy('dash')

    def get_object(self, queryset=None):
        order = super().get_object(queryset)

        if order.items.first().product.seller != self.request.user:
            return None
        if order.items.count() != 1 or order.items.first().product.seller != self.request.user:
            return None
        return order

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        if order:
            return super().get(request, *args, **kwargs)
        return redirect('ordered-products')
