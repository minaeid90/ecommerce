from django.db import models
from django.db.models.signals import pre_save,post_save


from ecommerce.utils import unique_order_id_generator

from carts.models import Cart

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class Order(models.Model):

    order_id = models.CharField(max_length=150, blank=True)
    # bill_profile
    # bill_address
    cart = models.ForeignKey(Cart)
    status = models.CharField(
        default='created', max_length=150, choices=ORDER_STATUS_CHOICES)

    shipping_total = models.DecimalField(
        default=5.99, max_digits=100, decimal_places=2)
    order_total = models.DecimalField(
        default=5.99, max_digits=100, decimal_places=2)


    def __str__(self):
        return self.order_id

    def update_total(self):
        self.order_total = self.cart.total + self.shipping_total
        self.save()
        return self.order_total


def order_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


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
