from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser


class UserAdminConfig(UserAdmin):
    search_field = ('email', 'user_name', 'first_name')
    list_filter = ('email', 'user_name', 'first_name', 'height')
    ordering = ('-start_date',)
    list_display = ('user_name', 'email', 'sex', 'is_admin', 'is_active')
    fieldsets = (
        ('General',{'fields': ('email', 'first_name', 'user_name')}),
        ('Permission', {'fields': ('is_admin', 'is_superuser', 'is_active')}),
        ('Personal', {'fields': ('height','birthday', 'meal_plan')})
    )
    add_fieldsets = (
        ("Login Info", {'classes': 'wide', 'fields':('email', 'user_name','password1', 'password2')}),
        ("Health Info", {'classes': 'wide', 'fields': ('birthday', 'height', 'weight', 'sex')}),

    )


# admin.site.register(NewUser)
admin.site.register(NewUser, UserAdminConfig)
