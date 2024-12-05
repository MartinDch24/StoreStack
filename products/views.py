from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import CreateView, DeleteView
from products.models import Product
from products.forms import ProductCreateForm, ProductEditForm


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
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product-detail.html'
    context_object_name = 'product'


class ProductEditView(UpdateView, LoginRequiredMixin):
    model = Product
    form_class = ProductEditForm
    template_name = 'products/product-edit.html'
    context_object_name = 'product'
    success_url = reverse_lazy('user-products')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()

        if product.seller != self.request.user:
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product-delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('dash')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()

        if product.seller != self.request.user:
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

