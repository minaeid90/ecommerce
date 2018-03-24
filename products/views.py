from django.shortcuts import render, Http404
from django.views.generic import list, detail

from .models import Product
from carts.models import Cart


class ProductListView(list.ListView):
    model = Product
    # queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)

        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('slug')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")

        return instance


class ProductDetailView(detail.DetailView):
    model = Product
    template_name = "products/detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, is_new = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
