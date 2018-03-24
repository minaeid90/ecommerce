from django.conf.urls import url

from .views import SearchProductListView

urlpatterns = [

    url(r'^$', SearchProductListView.as_view(), name='query'),
    # url(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail'), 

]