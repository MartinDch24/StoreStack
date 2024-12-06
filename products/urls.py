from django.urls import path, include
from products import views

urlpatterns = [
    path('my-products/', views.SellerProductsView.as_view(), name='seller-products'),
    path('create/', views.ProductCreateView.as_view(), name='product-add'),
    path('product/<int:pk>/', include([
        path('', views.ProductDetailView.as_view(), name='product-detail'),
        path('edit/', views.ProductEditView.as_view(), name='product-edit'),
        path('delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    ])),
]
