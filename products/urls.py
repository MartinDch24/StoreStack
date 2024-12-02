from django.urls import path
from products import views

urlpatterns = [
    path('create/', views.ProductCreateView.as_view(), name='product-add'),
]
