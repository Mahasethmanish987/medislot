from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):

    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ("email", "username", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone_number", "role")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "first_name",
                "last_name",
                "phone_number",
                "role",
                "password1",
                "password2",
                "is_staff",
                "is_active",
            ),
        }),
    )

    search_fields = ("email", "username")
    ordering = ("email",)

    filter_horizontal = ()

admin.site.register(User, UserAdmin)    