from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _

from .models import Driver, MyUser
from .forms import UserChangeForm, UserCreationForm

# Register your models here.


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', '__unicode__', 'is_superuser', 'is_admin',
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


class DriverAdmin(admin.ModelAdmin):
    list_display = ('id', '__unicode__', 'is_active',
                    'average_rating',)
    list_filter = ('is_active', 'trips_completed',)
    fields = ('user', 'is_active', 'rating', 'trips_completed',
              'created', 'modified',)
    readonly_fields = ('created', 'modified',)
    actions = ('activate', 'disable',)

    class Meta:
        model = Driver

    def activate(self, request, queryset):
        queryset.update(is_active=True)
    activate.short_description = _("Activate selected drivers")

    def disable(self, request, queryset):
        queryset.update(is_active=False)
    disable.short_description = _("Disable selected drivers")

admin.site.register(Driver, DriverAdmin)
admin.site.unregister(Group)
