
from django.db import models
from django.db.models.signals import pre_save, post_save

import random
import os

from ecommerce.utils import unique_slug_generator


class ProductQuerySet(models.query.QuerySet):
    
    def active(self):
        return self.filter(active=True)

class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, pk):
        queryset = self.filter(pk=pk)
        if queryset.count() == 1:
            return queryset.first()
        return None

    def search(self, query):
        lookups = ( models.Q(title__icontains=query) | 
                    models.Q(description__icontains=query) | 
                    models.Q(price__icontains=query) |
                    models.Q(tag__title__icontains=query))

        return self.all().filter(lookups).distinct()
        
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
            new_filename=new_filename, 
            final_filename=final_filename
)
class Product(models.Model):
    
    title           = models.CharField(max_length=150)
    slug            = models.SlugField(blank=True, unique=True)
    description     = models.TextField()
    price           = models.DecimalField(max_digits=5, decimal_places=2)
    image           = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    active          = models.BooleanField(default=True)

    objects = ProductManager() 

    def __str__(self):
        return self.title

 
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('products:detail', kwargs={'slug': self.slug})


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)