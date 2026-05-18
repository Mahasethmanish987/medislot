from django import forms 
from .models import User


class UserRegistrationForm(forms.ModelForm): 
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "w-full p-2 border rounded"
    }))
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "w-full p-2 border rounded"
    }))
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "w-full p-2 border rounded"
    }))
    
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "w-full p-2 border rounded"
    }))
    
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        "class": "w-full p-2 border rounded"
    }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "w-full p-2 border rounded"
    }))
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "w-full p-2 border rounded"
    }))

    class Meta: 
        model = User
        fields = [
            'email', 
            'username', 
            'first_name', 
            'last_name', 
            'phone_number', 
            'password',
            'confirm_password'
            ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already in use.")
        return username
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number is already in use.")
        return phone_number
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError("First name is required.")
        return first_name
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError("Last name is required.")
        return last_name
    def clean_password(self):
      
      password = self.cleaned_data.get("password")
      if not password:
        raise forms.ValidationError("Password is required.")
      if len(password) < 8:
        raise forms.ValidationError("Password must be at least 8 characters long.")
      return password
    
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get("confirm_password")
        if not confirm_password:
            raise forms.ValidationError("Please confirm your password.")
        if len(confirm_password) < 8:
           raise forms.ValidationError("Password must be at least 8 characters long.") 
        return confirm_password
     
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")