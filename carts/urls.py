from django.conf.urls import url

from .views import cart_home, cart_update, checkout, success

urlpatterns = [

    url(r'^$', cart_home, name='home'),
    url(r'^update/$', cart_update, name='update'),
    url(r'^checkout/$', checkout, name='checkout'),
    url(r'^success/$', success, name='success'),
    
   
]
  