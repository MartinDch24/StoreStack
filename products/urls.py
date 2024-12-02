from django.urls import path
from products import views

urlpatterns = [
    path('my-products/', views.UserProductsView.as_view(), name='user-products'),
    path('create/', views.ProductCreateView.as_view(), name='product-add'),
]
