from django.shortcuts import render,redirect
from .forms import UserRegistrationForm, UserLoginForm
from .services.user_service import UserService
from .models import User
from django.db import transaction
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from .utils import user_redirect_based_on_role
from django.http import HttpResponse


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
                   password=user_form.cleaned_data['password'],
                   confirm_password=user_form.cleaned_data['confirm_password']
               )
               return redirect('myapp:index')
            except Exception as e:
                messages.error(request, f"An error occurred during registration: {str(e)}")
                print(f"Error during user registration: {str(e)}")
               
               
        context = {
        'user_form':user_form
       }
    else:
        context = {
            'user_form': UserRegistrationForm()
        }    
    return render(request, "accounts/user_register.html", context)

def user_login(request): 
    login_form= UserLoginForm(request.POST or None)
    if request.method == "POST":
      if login_form.is_valid(): 
          user=authenticate(
              request, 
              email= login_form.cleaned_data.get('email'), 
              password=login_form.cleaned_data.get('password')
              )
          print('Authentication result:', user)
          print('email:', login_form.cleaned_data.get('email'), 'password:', login_form.cleaned_data.get('password'))
          if user is not None: 
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('accounts:user_redirect')
          messages.error(request, "Invalid email or password.")
       
    context = {
        'login_form': login_form
    }
    return render(request, "accounts/login.html", context)

def user_logout(request):
   
    if not request.user.is_authenticated:
        messages.error(request, "You are not logged in.")
        return redirect('myapp:index')
    
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('myapp:index')

def user_redirect(request):
    if not request.user.is_authenticated:
        messages.error(request, "You are not logged in.")
        return redirect('myapp:index')
    
    redirect_url = user_redirect_based_on_role(request.user)
    return redirect(redirect_url)


def user_dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "You are not logged in.")
        return redirect('myapp:index')
    return HttpResponse("User Dashboard")

def doctor_dashboard(request): 
    if not request.user.is_authenticated:
        messages.error(request, "You are not logged in.")
        return redirect('myapp:index')
    return HttpResponse("Doctor Dashboard")