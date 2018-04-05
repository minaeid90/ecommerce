import math
from django.db import models
from django.db.models.signals import pre_save,post_save


from ecommerce.utils import unique_order_id_generator

from carts.models import Cart
from billing.models import BillingProfile
from address.models import Address

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)

class OrderManger(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
                billing_profile=billing_profile, 
                cart=cart_obj, 
                active=True,
                status='created')
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                    billing_profile=billing_profile, 
                    cart=cart_obj)
            created = True
        return obj, created

class Order(models.Model):

    order_id            = models.CharField(max_length=150, blank=True)
    billing_profile     = models.ForeignKey(BillingProfile, null=True, blank=True)
    billing_address     = models.ForeignKey(Address, related_name='billing_address', null=True, blank=True)
    shipping_address    = models.ForeignKey(Address, related_name='shipping_address', null=True, blank=True)
    cart                = models.ForeignKey(Cart)
    status              = models.CharField(default='created', max_length=150, choices=ORDER_STATUS_CHOICES)

    shipping_total      = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    order_total         = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    active              = models.BooleanField(default=True)

    objects = OrderManger()


    def __str__(self):
        return self.order_id

    def update_total(self):
        new_total = math.fsum([self.cart.total, self.shipping_total])
        self.order_total = format(new_total, '.2f')
        self.save()
        return self.order_total

    def check_done(self):
        billing_profile = self.billing_profile
        billing_address = self.billing_address
        shipping_address = self.shipping_address
        total = self.order_total
        
        if billing_profile and billing_address and shipping_address and total>0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = 'paid'
            self.save()
        return self.status


def order_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    
        qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
        if qs.exists():
            qs.update(active=False)

pre_save.connect(order_pre_save_receiver, sender=Order)

def cart_post_save_receiver(sender, instance, created, *args, **kwargs):
    if not created:
        # cart_obj = instance
        #cart_total = instance.total
        #cart_id = instance.
        qs = Order.objects.filter(cart__id=instance.id)
        if qs.count() == 1:
            order_obj=qs.first()
            order_obj.update_total()

post_save.connect(cart_post_save_receiver,sender=Cart)

def order_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()

post_save.connect(order_post_save,sender=Order)
