from django.shortcuts import render
from django.views.generic import ListView


from products.models import Product

class SearchProductListView(ListView):
    model = Product
    # queryset = Product.objects.all()
    template_name = "search/products.html"

    
    # def get_context_data(self, **kwargs):
    #     context = super(ProductListView, self).get_context_data(**kwargs)
    #     # add variables to context dictionary
    #     return context

    def get_queryset(self):

        request = self.request
        query = request.GET.get('q', '')
        
        queryset = Product.objects.search(query)
        
        return queryset