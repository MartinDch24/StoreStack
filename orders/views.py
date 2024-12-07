from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from orders.models import Order, OrderItem
from products.models import Product


class SellerOrdersView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'orders/seller-orders.html'
    context_object_name = 'orders'
    permission_required = 'orders.view_order'
    paginate_by = 5

    def get_queryset(self):
        return Order.for_seller(self.request.user)
