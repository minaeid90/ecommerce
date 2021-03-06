from django.shortcuts import redirect, render
from django.http import HttpResponse

from accounts.forms import GuestForm, LoginForm
from accounts.models import Guest
from address.forms import AddressForm
from address.models import Address
from billing.models import BillingProfile
from orders.models import Order
from products.models import Product

from .models import Cart


def cart_home(request):

    cart_obj, is_new = Cart.objects.new_or_get(request)
    context = {
        'cart': cart_obj,
    }
    return render(request, 'carts/cart.html', context)


def cart_update(request):
   
    product_id = request.POST.get('product_id')
    try:
        product_obj = Product.objects.get(id=product_id)
    except Product.DoesNotExist():
        print("Product doesn't already there.")
    cart_obj, is_new = Cart.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)
    else:
        cart_obj.products.add(product_obj)
    request.session['cart_items'] = cart_obj.products.count()
    return redirect('cart:home')


def checkout(request):
    cart_obj, is_new_cart = Cart.objects.new_or_get(request)
    order_obj = None
    if is_new_cart or cart_obj.products.count()==0:
        return redirect('cart:home')
    
    user = request.user
    billing_profile = None
    if user.is_authenticated:
        billing_profile = None

    login_form = LoginForm()
    guest_login_form = GuestForm()
    address_form = AddressForm()
    billing_address_form = AddressForm()

    billing_profile, created = BillingProfile.objects.new_or_get(request)

    billing_address_id = request.session.get('billing_address_id')
    shipping_address_id = request.session.get('shipping_address_id')
    
    address_qs = None
    if billing_profile is not None:
        address_qs = Address.objects.filter(billing_profile=billing_profile)
        # shipping_address_qs = address_qs.filter(address_type='shipping')
        # billing_address_qs = address_qs.filter(address_type='billing')
        
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']        
        if billing_address_id or shipping_address_id:
            order_obj.save()
    if request.method == 'POST':
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            del request.session['cart_id']
            request.session['cart_items'] = 0
            return redirect('/cart/success')
   
    context = {
        'object':order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_login_form':guest_login_form,
        'address_form': address_form,
        'billing_address_form': billing_address_form,       
        'address_qs' : address_qs,
    }

    return render(request,'carts/checkout.html',context)

def success(request):
    return render(request, 'carts/success.html', {})