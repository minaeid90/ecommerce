from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm, LoginForm, RegisterForm

from django.contrib.auth import authenticate, login, get_user_model


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

def login_page(request):
    form = LoginForm(request.POST or None)

 

    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username= username, password= password)
        if user is not None:
            print('User login successufly')
            login(request,user)
            redirect('/login')
        else:
            print("Error")

    context = {'form': form}
    
    return render(request, "auth/login.html", context)


users = get_user_model()
def register_page(request):

    form = RegisterForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
  
        new_user = users.objects.create_user(username, email, password)
        new_user.save()
        redirect('/')

    context = {'form': form}
    return render(request, "auth/register.html", context)
    