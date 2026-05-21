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
            'password'
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

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


class UserLoginForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "Enter your email"
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "Enter your password"
            }
        )
    )

class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "phone_number", "role")

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")

        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")

        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # 🔥 HASHING

        if commit:
            user.save()

        return user

class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = "__all__"        