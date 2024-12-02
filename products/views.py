from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from products.models import Product
from products.forms import ProductCreateForm


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'products/product-add.html'
    success_url = reverse_lazy('dash')
