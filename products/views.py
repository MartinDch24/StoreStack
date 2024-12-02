from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from products.models import Product
from products.forms import ProductCreateForm


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = 'products/product-add.html'
    success_url = reverse_lazy('dash')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class UserProductsView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/user-products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)