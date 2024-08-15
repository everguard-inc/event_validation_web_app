from django.contrib import admin
from django.contrib.auth import get_user_model, forms
from django.contrib.auth import admin as auth_admin


User = get_user_model()


# Register your models here.
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        (
            "Permissions",
            {
                "fields": (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'is_superuser', 'date_joined')
    search_fields = ('username', )
    ordering = ('id', )
