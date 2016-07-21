from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from reservations.models import Reservation


class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    reservation_url = serializers.SerializerMethodField()
    user = serializers.CharField(source='user.full_name', read_only=True)
    user_url = serializers.SerializerMethodField()
    user_phone_number = serializers.CharField(
        source='user.phone_number', read_only=True)
    user_profile_pic = serializers.ImageField(source='user.profile_picture')
    driver = serializers.CharField(source='driver.full_name',
                                   read_only=True)
    driver_id = serializers.CharField(source='driver.id', read_only=True)
    driver_url = serializers.SerializerMethodField()
    driver_phone_number = serializers.CharField(
        source='driver.phone_number', read_only=True)
    driver_profile_pic = serializers.ImageField(
        source='driver.profile_picture')
    # destination_address = serializers.CharField(source='address_from_query')
    pick_up_interval = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ('id', 'reservation_url', 'user', 'user_url',
                  'user_phone_number', 'user_profile_pic',
                  'get_pending_drivers_info', 'driver',
                  'driver_url', 'driver_id', 'driver_phone_number',
                  'driver_profile_pic', 'status_verbose',
                  'pick_up_interval', 'start_amount', 'final_amount',
                  'start_query', 'destination_query', 'start_long',
                  'start_lat', 'end_long', 'end_lat', 'travel_distance',
                  'created', 'modified',
                  # 'start_address', 'destination_address',
                  )

    def get_reservation_url(self, obj):
        return api_reverse('reservation_detail_api',
                           kwargs={'reservation_id': obj.id},
                           request=self.context['request'])

    def get_user_url(self, obj):
        return api_reverse('user_account_detail_api',
                           kwargs={'id': obj.user.id},
                           request=self.context['request'])

    def get_driver_url(self, obj):
        if obj.driver:
            return api_reverse('user_driver_detail_api',
                               kwargs={'id': obj.driver.id},
                               request=self.context['request'])
        return None

    def get_pick_up_interval(self, obj):
        # %l:%M %p (removes leading 0)
        return obj.pick_up_interval.strftime("%I:%M %p")


class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'pick_up_interval', 'start_amount', 'start_long',
                  'start_lat', 'start_query', 'destination_query',)
