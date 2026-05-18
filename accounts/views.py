from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from .services.user_service import UserService
from .models import User
from django.db import transaction
from django.contrib import messages 


def user_register(request): 
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in.")
        return redirect('myapp:index')
    
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            try: 
             with transaction.atomic(): 
               UserService(request).create_user(
                   email=user_form.cleaned_data['email'],
                   username=user_form.cleaned_data['username'],
                   first_name=user_form.cleaned_data['first_name'],
                   last_name=user_form.cleaned_data['last_name'],
                   phone_number=user_form.cleaned_data['phone_number'],
                   role=User.PATIENT,
                   password=user_form.cleaned_data['password']
               )
               return redirect('myapp:index')
            except Exception as e:
                messages.error(request, f"An error occurred during registration: {str(e)}")
    context = {
        'user_form': UserRegistrationForm()
    }
    return render(request, "accounts/register.html", context)