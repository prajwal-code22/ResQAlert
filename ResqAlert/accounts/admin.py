from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):

    model = User

    # Fields shown when editing existing user
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Information', {
            'fields': ('role', 'phone', 'responder_category', 'is_available'),
        }),
    )

    # Fields shown when creating new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Information', {
            'fields': ('role', 'phone', 'responder_category', 'is_available'),
        }),
    )

    list_display = ('username', 'email', 'role', 'phone', 'is_available')
    list_filter = ('role', 'is_available')


admin.site.register(User, CustomUserAdmin)