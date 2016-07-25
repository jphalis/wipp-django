from __future__ import absolute_import

from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.validators import UniqueValidator

from push_notifications.models import APNSDevice, GCMDevice
from push_notifications.fields import hex_re
from push_notifications.fields import UNSIGNED_64BIT_INT_MAX_VALUE


class HexIntegerField(IntegerField):
    """
    Store an integer represented as a hex string of form "0x01".
    """

    def to_internal_value(self, data):
        # validate hex string and convert it to the unsigned
        # integer representation for internal use
        try:
            data = int(data, 16)
        except ValueError:
            raise ValidationError("Device ID is not a valid hex number")
        return super(HexIntegerField, self).to_internal_value(data)

    def to_representation(self, value):
        return value


class DeviceSerializerMixin(ModelSerializer):
    class Meta:
        fields = ("user", "device_type", "registration_id", "device_id",
                  "date_created",)
        read_only_fields = ("user", "date_created",)
        extra_kwargs = {"is_active": {"default": True}}


class APNSDeviceSerializer(ModelSerializer):
    class Meta(DeviceSerializerMixin.Meta):
        model = APNSDevice

    def validate_registration_id(self, value):
        # iOS device tokens are 256-bit hexadecimal (64 characters).
        # In 2016 Apple is increasing
        # iOS device tokens to 100 bytes hexadecimal (200 characters).

        if hex_re.match(value) is None or len(value) not in (64, 200):
            raise ValidationError("Registration ID (device token) is invalid")
        return value


class GCMDeviceSerializer(ModelSerializer):
    device_id = HexIntegerField(
        help_text="ANDROID_ID / TelephonyManager.getDeviceId() (e.g: 0x01)",
        style={'input_type': 'text'},
        required=False)

    class Meta(DeviceSerializerMixin.Meta):
        model = GCMDevice
        extra_kwargs = {
            # Work around an issue with validating the uniqueness of
            # registration ids of up to 4k
            'registration_id': {
                'validators': [
                    UniqueValidator(queryset=GCMDevice.objects.all())
                ]
            }
        }

    def validate_device_id(self, value):
        # device ids are 64 bit unsigned values
        if value > UNSIGNED_64BIT_INT_MAX_VALUE:
            raise ValidationError("Device ID is out of range")
        return value
