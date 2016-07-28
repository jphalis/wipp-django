from django.contrib import admin

from .models import Reservation

# Register your models here.


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'driver', 'reservation_status',
                    'start_amount']
    list_filter = ['reservation_status']
    search_fields = ['id', 'driver__user__get_full_name',
                     'user__get_full_name']
    fields = ['id', 'reservation_status', 'user', 'driver', 'pending_drivers',
              'start_query', 'destination_query', 'pick_up_interval',
              'start_amount', 'final_amount', 'start_long', 'start_lat',
              'created', 'modified']
    readonly_fields = ['id', 'created', 'modified']
    ordering = ['-created']

    class Meta:
        model = Reservation

admin.site.register(Reservation, ReservationAdmin)
