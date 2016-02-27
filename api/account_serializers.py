from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from accounts.models import MyUser, Driver


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser.objects.create(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyUserSerializer(serializers.HyperlinkedModelSerializer):
    account_url = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)

    class Meta:
        model = MyUser
        fields = ('id', 'account_url', 'email', 'first_name', 'last_name',
                  'profile_picture', 'phone_number', 'is_active', 'is_admin',
                  'date_joined', 'modified',)

    def get_account_url(self, obj):
        request = self.context['request']
        kwargs = {'id': obj.id}
        return api_reverse('user_account_detail_api', kwargs=kwargs,
                           request=request)


class DriverCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.id', read_only=True)

    class Meta:
        model = Driver
        fields = ('user',)


class DriverSerializer(serializers.HyperlinkedModelSerializer):
    driver_url = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    profile_picture = serializers.ReadOnlyField(
        source="user.default_profile_picture")
    phone_number = serializers.CharField(
        source="user.phone_number")

    class Meta:
        model = Driver
        fields = ('id', 'driver_url', 'is_active', 'average_rating',
                  'email', 'first_name', 'last_name',
                  'profile_picture', 'phone_number',
                  'created', 'modified',)

    def get_driver_url(self, obj):
        request = self.context['request']
        kwargs = {'id': obj.id}
        return api_reverse('user_driver_detail_api', kwargs=kwargs,
                           request=request)
