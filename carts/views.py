from django.shortcuts import render, redirect

from .models import Cart
from products.models import Product


def cart_home(request):

    cart_obj, is_new = Cart.objects.new_or_get(request)
    context = {
        'cart': cart_obj,
    }

    return render(request, 'carts/cart.html', context)


def cart_update(request):
    print(request.POST)
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
