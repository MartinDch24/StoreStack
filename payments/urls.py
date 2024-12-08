from django.urls import path, include
from payments import views

urlpatterns = [
    path('add/', views.PaymentMethodCreateView.as_view(), name='payment-add'),
    path('payment-methods/', views.PaymentMethodsView.as_view(), name='payments-detail'),
    path('<int:pk>/', include([
        path('edit/', views.PaymentMethodEditView.as_view(), name='payment-edit'),
        path('delete/', views.PaymentMethodDeleteView.as_view(), name='payment-delete'),
    ]))
]
