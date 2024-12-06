from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from orders.models import Order


class SellerOrdersView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'orders/seller-orders.html'
    context_object_name = 'orders'
    permission_required = 'orders.view_order'
    paginate_by = 5

    def get_queryset(self):
        return Order.for_seller(self.request.user)
