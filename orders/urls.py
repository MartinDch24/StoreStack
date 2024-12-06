from django.urls import path
from orders.views import SellerOrderListView

urlpatterns = [
    path('seller-orders/', SellerOrdersView.as_view(), name='seller-orders'),
]
