from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from products.models import Product
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

        return context
