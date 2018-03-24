from django import forms
from django.contrib.auth import get_user_model

class ContactForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(
        attrs = 
            {
            "class":"form-control",
            "placeholder":"Your full name"
            }
         )
    )
    email = forms.EmailField(widget=forms.EmailInput(
        attrs = 
            {
            "class":"form-control", 
            "placeholder":"Your email address"
            }
        )
    )
    message = forms.CharField(widget=forms.Textarea(
        attrs = 
            {
            "class":"form-control",
            "placeholder":"Your message"
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not "@gmail.com" in email:
            raise forms.ValidationError('Email must be a gmail') 
        return email

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


users = get_user_model() 

class RegisterForm(forms.Form):

    username = forms.CharField()
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords must match.')
        return data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = users.objects.filter(username = username)
   
        if qs.exists():
            raise forms.ValidationError('Username already exists.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = users.objects.filter(email = email)
   
        if qs.exists():
            raise forms.ValidationError('E-mail already exists.')
        return email


     