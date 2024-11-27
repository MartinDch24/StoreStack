from django.views.generic import TemplateView, ListView
from products.models import Product


class HomePageView(TemplateView):
    template_name = "common/index.html"


class DashboardView(ListView):
    model = Product
    template_name = 'common/dashboard.html'
    context_object_name = 'products'
    paginate_by = 5
