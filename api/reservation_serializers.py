from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from reservations.models import Reservation


# class ReservationCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reservation
#         fields = ('id', 'email', 'password',)

#     def perform_create(self, validated_data):
#         reservation = Reservation.objects.create(
#             email=validated_data['email']
#         )
#         reservation.save()
#         return reservation


class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.CharField(source='user.id', read_only=True)
    user_url = serializers.SerializerMethodField()
    driver = serializers.CharField(source='driver.user.id',
                                   read_only=True)
    driver_url = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)

    class Meta:
        model = Reservation
        fields = ('id', 'user', 'user_url', 'driver', 'driver_url',
                  'reservation_status', 'longitude', 'latitude', 'is_active',
                  'is_accepted', 'is_completed', 'created', 'modified',)

    def get_user_url(self, obj):
        request = self.context['request']
        kwargs = {'id': obj.user.id}
        return api_reverse('user_account_detail_api', kwargs=kwargs,
                           request=request)

    def get_driver_url(self, obj):
        request = self.context['request']
        kwargs = {'id': obj.driver.user.id}
        return api_reverse('user_account_detail_api', kwargs=kwargs,
                           request=request)
