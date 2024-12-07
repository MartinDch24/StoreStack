from django.urls import path
from orders import views

urlpatterns = [
    path('seller-orders/', views.SellerOrdersView.as_view(), name='seller-orders'),
    path('api/cart/add/<int:product_id>/', views.AddToCartAPIView.as_view(), name='add-to-cart'),
]
