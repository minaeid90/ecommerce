from django.contrib import admin
from .models import Product



class ProductAdmin(admin.ModelAdmin):
   
    list_display = ('title', 'slug')
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)

admin.site.register(Product, ProductAdmin)


