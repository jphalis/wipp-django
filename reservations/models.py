from __future__ import unicode_literals
from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel
from core.utils import (address_from_query, coordinates_from_query,
                        travel_distance, verbose_address)

# Create your models here.


class ReservationManager(models.Manager):
    def pending(self):
        """
        Returns all requests with a status of:
        Pending... or Select Driver.
        """
        return super(ReservationManager, self).get_queryset() \
            .filter(Q(reservation_status=Reservation.PENDING) |
                    Q(reservation_status=Reservation.SELECT),
                    pick_up_interval__gte=datetime.now().time()) \
            .select_related('user')

    def own_user(self, user):
        """
        Returns all requests for the current user.
        """
        return super(ReservationManager, self).get_queryset() \
            .filter(user=user).select_related('user') \
            .prefetch_related('pending_drivers')

    def own_driver(self, driver):
        """
        Returns all requests for the current driver.
        """
        return super(ReservationManager, self).get_queryset() \
            .filter(driver=driver).select_related('driver')


class Reservation(TimeStampedModel):
    PENDING = 0
    NEGOTIATING = 1
    ACCEPTED = 2
    COMPLETED = 3
    CANCELED = 4
    SELECT = 5

    RESERVATION_STATUSES = (
        (PENDING, _('Pending...')),
        (NEGOTIATING, _('Negotiating')),
        (ACCEPTED, _('Accepted')),
        (COMPLETED, _('Completed')),
        (CANCELED, _('Canceled')),
        (SELECT, _('Select Driver')),
    )
    reservation_status = models.IntegerField(
        choices=RESERVATION_STATUSES, default=PENDING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                               related_name='driver')
    pending_drivers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                             related_name='pending_drivers',
                                             blank=True)
    pick_up_interval = models.TimeField()
    start_amount = models.DecimalField(max_digits=18, decimal_places=2,
                                       default=0.00)
    final_amount = models.DecimalField(max_digits=18, decimal_places=2,
                                       default=0.00)
    start_query = models.CharField(max_length=100, null=True, blank=True)
    destination_query = models.CharField(max_length=100, null=True, blank=True)
    start_long = models.DecimalField(max_digits=12, decimal_places=8,
                                     null=True, blank=True)
    start_lat = models.DecimalField(max_digits=12, decimal_places=8,
                                    null=True, blank=True)
    end_long = models.DecimalField(max_digits=12, decimal_places=8, null=True)
    end_lat = models.DecimalField(max_digits=12, decimal_places=8, null=True)

    objects = ReservationManager()

    class Meta:
        app_label = 'reservations'

    def __unicode__(self):
        return u"{}".format(self.user.id)

    @cached_property
    def get_pending_drivers_info(self):
        """
        Returns the values of the pending drivers for each request.
        """
        return self.pending_drivers.values(
            'id', 'email', 'full_name', 'phone_number', 'profile_picture')

    @cached_property
    def net_change_amount(self):
        """
        Returns the difference between the start amount and the final amount.
        """
        if self.reservation_status == self.COMPLETED:
            return float("{0:.2f}".format(
                float(self.final_amount) - float(self.start_amount)))
        return 0

    @cached_property
    def status_verbose(self):
        """
        Returns the verbose of the reservation status.
        """
        return dict(Reservation.RESERVATION_STATUSES)[self.reservation_status]

    @cached_property
    def verbose_address(self):
        """
        Returns the address corresponding to a set of coordinates.
        """
        return verbose_address(query=self.start_lat, longitude=self.start_long)

    @cached_property
    def address_from_query(self):
        """
        Returns the address of the destination query.
        """
        return address_from_query(query=self.destination_query)

    @cached_property
    def start_address(self):
        """
        Returns the address of the starting location.
        """
        if self.start_lat and self.start_long:
            location = verbose_address(
                latitude=self.start_lat, longitude=self.start_long)
        else:
            location = address_from_query(query=self.start_query)
        return location

    @cached_property
    def coordinates_from_query(self):
        """
        Returns the coordinates for the destination query.
        """
        return coordinates_from_query(query=self.destination_query)

    @cached_property
    def travel_distance(self):
        """
        Returns the total travel distance for the request.
        """
        return travel_distance(start_lat=self.start_lat,
                               start_lng=self.start_long,
                               end_lat=self.end_lat,
                               end_lng=self.end_long,
                               validator=False)
