from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .fields import HexIntegerField


@python_2_unicode_compatible
class Device(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    device_type = models.CharField(max_length=255, verbose_name=_("Device"),
                                   blank=True, null=True)
    date_created = models.DateTimeField(verbose_name=_("Creation date"),
                                        auto_now_add=True, null=True)
    is_active = models.BooleanField(
        verbose_name=_("Is active"), default=True,
        help_text=_("Inactive devices will not be sent notifications"))

    class Meta:
        abstract = True

    def __str__(self):
        return self.device_type or \
            str(self.device_id or "") or \
            "%s for %s" % (self.__class__.__name__,
                           self.user or "unknown user")


# I P H O N E
class APNSDeviceManager(models.Manager):
    def get_queryset(self):
        return APNSDeviceQuerySet(self.model)


class APNSDeviceQuerySet(models.query.QuerySet):
    def send_message(self, message, **kwargs):
        if self:
            from .apns import apns_send_bulk_message
            reg_ids = list(self.filter(is_active=True).values_list(
                'registration_id', flat=True))
            return apns_send_bulk_message(registration_ids=reg_ids,
                                          alert=message, **kwargs)


class APNSDevice(Device):
    device_id = models.UUIDField(
        verbose_name=_("Device ID"), blank=True, null=True, db_index=True,
        help_text="UDID / UIDevice.identifierForVendor()")
    registration_id = models.CharField(verbose_name=_("Registration ID"),
                                       max_length=200, unique=True)

    objects = APNSDeviceManager()

    class Meta:
        verbose_name = _("APNS device")

    def send_message(self, message, **kwargs):
        from .apns import apns_send_message

        return apns_send_message(registration_id=self.registration_id,
                                 alert=message, **kwargs)


def get_expired_tokens():
    from .apns import apns_fetch_inactive_ids
    return apns_fetch_inactive_ids()


# A N D R O I D
class GCMDeviceManager(models.Manager):
    def get_queryset(self):
        return GCMDeviceQuerySet(self.model)


class GCMDeviceQuerySet(models.query.QuerySet):
    def send_message(self, message, **kwargs):
        if self:
            from .gcm import gcm_send_bulk_message

            data = kwargs.pop("extra", {})
            if message is not None:
                data["message"] = message

            reg_ids = list(self.filter(is_active=True).values_list(
                'registration_id', flat=True))
            return gcm_send_bulk_message(registration_ids=reg_ids, data=data,
                                         **kwargs)


class GCMDevice(Device):
    # device_id cannot be a reliable primary key as fragmentation between
    # different devices can make it turn out to be null and such:
    # http://android-developers.blogspot.co.uk/2011/03/identifying-app-installations.html
    device_id = HexIntegerField(
        verbose_name=_("Device ID"), blank=True, null=True, db_index=True,
        help_text=_("ANDROID_ID / TelephonyManager.getDeviceId()"))
    registration_id = models.TextField(verbose_name=_("Registration ID"))

    objects = GCMDeviceManager()

    class Meta:
        verbose_name = _("GCM device")

    def send_message(self, message, **kwargs):
        from .gcm import gcm_send_message
        data = kwargs.pop("extra", {})
        if message is not None:
            data["message"] = message
        return gcm_send_message(registration_id=self.registration_id,
                                data=data, **kwargs)
