from django.urls import path
from orders import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<int:pk>', views.AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('checkout/<int:product_id>/', views.CheckoutView.as_view(), name='single-product-checkout'),
    path('my-orders/', views.MyOrdersView.as_view(), name='my-orders'),
    path('ordered-products/', views.OrderedProductsView.as_view(), name='ordered-products'),
    path('order/<int:pk>/update/', views.OrderStatusUpdateView.as_view(), name='update-order-status'),
]
