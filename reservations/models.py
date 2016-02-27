from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.models import Driver
from core.models import TimeStampedModel

# Create your models here.


class Reservation(TimeStampedModel):
    RESERVATION_STATUSES = (
        (0, _('Pending')),
        (1, _('Negotiating')),
        (2, _('Accepted')),
        (3, _('Completed'))
    )
    reservation_status = models.IntegerField(
        choices=RESERVATION_STATUSES, default=RESERVATION_STATUSES[0][0])
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    driver = models.ForeignKey(Driver, null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    def __unicode__(self):
        return u"{}".format(self.user.id)
