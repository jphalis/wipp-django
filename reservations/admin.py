from django.contrib import admin

from .models import Reservation

# Register your models here.


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'driver', 'reservation_status', 'is_active']
    list_filter = ['reservation_status']
    search_fields = ['id', 'driver__user__get_full_name',
                     'user__get_full_name']
    fields = ['id', 'user', 'driver', 'reservation_status', 'longitude',
              'latitude', 'is_active', 'created', 'modified']
    readonly_fields = ['id', 'longitude', 'latitude', 'created', 'modified']
    ordering = ['-created']

    class Meta:
        model = Reservation

admin.site.register(Reservation, ReservationAdmin)
