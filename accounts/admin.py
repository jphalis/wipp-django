from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _

from .models import MyUser
from .forms import UserChangeForm, UserCreationForm

# Register your models here.


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'email', 'is_superuser', 'is_admin',
                    'date_joined',)
    list_filter = ('is_active', 'is_admin',)
    readonly_fields = ('date_joined', 'last_login', 'modified',)
    fieldsets = (
        (None,
            {'fields': ('email', 'password',)}),
        ('Basic information',
            {'fields': ('first_name', 'last_name', 'phone_number',
                        'profile_picture',)}),
        ('Permissions',
            {'fields': ('is_active', 'is_admin',
                        'user_permissions')}),
        (_('Dates'),
            {'fields': ('date_joined', 'last_login', 'modified',)}),
    )

    add_fieldsets = (
        (None,
            {'classes': ('wide',),
             'fields': ('email', 'password1', 'password2',)}),
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)
    filter_horizontal = ('user_permissions',)
    actions = ('activate', 'disable',)

    def activate(self, request, queryset):
        queryset.update(is_active=True)
    activate.short_description = _("Activate selected users")

    def disable(self, request, queryset):
        queryset.update(is_active=False)
    disable.short_description = _("Disable selected users")

admin.site.register(MyUser, MyUserAdmin)
admin.site.unregister(Group)
