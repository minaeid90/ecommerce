from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm

def home_page(request):
    
    context = {
        "title": "Home Page",
        "content": "Welcome to Home page",
        
    }
   
    if request.user.is_authenticated:
        context['premium_content'] = "Cool Stuff"
    return render(request, 'home_page.html', context)

def blog_page(request):
    context = {
        
    }
  
    return render(request, 'blog.html', context)

def about_page(request):
    context = {
        "title": "About Page",
        "content": "Welcome to About page"
    }
    return render(request, 'home_page.html', context)

def contact_page(request):

    contact_form = ContactForm(request.POST or None)
    
    context = {
        "title": "Contact Page",
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    return render(request, 'contact.html', context)

