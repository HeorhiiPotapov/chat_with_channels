from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_select_related = ('profile', )
    list_display = ('email', 'name', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
