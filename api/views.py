from datetime import datetime
from geopy.geocoders import Nominatim

from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import generics, mixins, permissions, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response as RestResponse
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from accounts.models import Driver, MyUser
from core.mixins import AdminRequiredMixin, CacheMixin
from core.utils import check_dist_between_start_end
from reservations.models import Reservation
from .account_serializers import (AccountCreateSerializer, DriverSerializer,
                                  DriverCreateSerializer, MyUserSerializer)
from .auth_serializers import (PasswordResetSerializer,
                               PasswordResetConfirmSerializer,
                               PasswordChangeSerializer)
from .mixins import DefaultsMixin, FiltersMixin
from .pagination import AccountPagination, ReservationPagination
from .permissions import IsOwnerOrReadOnly, MyUserIsOwnerOrReadOnly
from .reservation_serializers import (ReservationCreateSerializer,
                                      ReservationSerializer)

# Create your views here.


class APIHomeView(AdminRequiredMixin, CacheMixin, DefaultsMixin, APIView):
    cache_timeout = 60 * 60 * 24 * 30

    def get(self, request, format=None):
        data = {
            'authentication': {
                'login': api_reverse('auth_login_api', request=request),
                'password_reset': api_reverse('rest_password_reset',
                                              request=request),
                'password_change': api_reverse('rest_password_change',
                                               request=request)
            },
            'accounts': {
                'count': MyUser.objects.all().count(),
                'url': api_reverse('user_account_list_api', request=request),
                'create_url': api_reverse('account_create_api',
                                          request=request),
                'profile_url': api_reverse(
                    'user_account_detail_api', request=request,
                    kwargs={'id': request.user.id}),
                'driver_url': api_reverse(
                    'user_driver_detail_api', request=request,
                    kwargs={'id': request.user.id})
            },
            'reservations': {
                'count': Reservation.objects.pending().count(),
                'url': api_reverse('reservation_list_api', request=request),
                'create_url': api_reverse('reservation_create_api',
                                          request=request),
                # 'status_check': api_reverse('get_reservation_status_api',
                #                             request=request),
            },
        }
        return RestResponse(data)


########################################################################
# ACCOUNTS                                                             #
########################################################################
class AccountCreateAPIView(generics.CreateAPIView):
    serializer_class = AccountCreateSerializer
    permission_classes = (permissions.AllowAny,)


class MyUserListAPIView(CacheMixin, DefaultsMixin, generics.ListAPIView):
    cache_timeout = 60 * 60 * 24
    pagination_class = AccountPagination
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()


class MyUserDetailAPIView(CacheMixin,
                          generics.RetrieveAPIView,
                          mixins.DestroyModelMixin,
                          mixins.UpdateModelMixin):
    cache_timeout = 60 * 5
    permission_classes = (
        permissions.IsAuthenticated,
        MyUserIsOwnerOrReadOnly,
    )
    serializer_class = MyUserSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def get_object(self):
        user_id = self.kwargs["id"]
        obj = get_object_or_404(MyUser, id=user_id)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DriverCreateAPIView(generics.CreateAPIView):
    serializer_class = DriverCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)


class DriverDetailAPIView(CacheMixin,
                          generics.RetrieveAPIView,
                          mixins.DestroyModelMixin,
                          mixins.UpdateModelMixin):
    cache_timeout = 60 * 5
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    serializer_class = DriverSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def get_object(self):
        user_id = self.kwargs["id"]
        obj = get_object_or_404(Driver, id=user_id)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


########################################################################
# AUTHENTICATION                                                       #
########################################################################
class PasswordResetView(generics.GenericAPIView):
    """
    Calls PasswordResetForm save method
    Accepts the following POST parameters: email
    Returns the success/fail message
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return RestResponse(
            {"success": "Password reset e-mail has been sent."},
            status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    Password reset e-mail link is confirmed, so this resets the user's password
    Accepts the following POST parameters: new_password1, new_password2
    Accepts the following Django URL arguments: token, uid
    Returns the success/fail message
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return RestResponse({"success": "Password has been reset."})


class PasswordChangeView(generics.GenericAPIView):
    """
    Calls SetPasswordForm save method
    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return RestResponse({"success": "New password has been saved."})


########################################################################
# RESERVATIONS                                                         #
########################################################################
class ReservationCreateAPIView(ModelViewSet):
    queryset = Reservation.objects.select_related('user').all()
    serializer_class = ReservationCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def perform_create(self, serializer):
        """
        Creates a reservation object. Validates the input address
        and returns the start/destination address for the driver/user
        to see.
        """
        if self.request.user.is_confirmed:
            geolocator = Nominatim()
            start_loc = None

            # Is there a start query?
            try:
                start_query = self.request.data.get('start_query')
            except:
                start_query = None

            # Are there starting coordinates?
            try:
                start_coordinates = (self.request.data.get('start_lat'),
                                     self.request.data.get('start_long'))
            except:
                start_coordinates = None

            # There is a start query...
            if start_query and not start_coordinates:
                start_adrs = geolocator.geocode(start_query, timeout=60)
                if start_adrs and start_adrs.latitude and start_adrs.longitude:
                    start_loc = (start_adrs.latitude, start_adrs.longitude)

            # There are starting coordinates...
            elif start_coordinates:
                start_loc = start_coordinates

            # Something went wrong...
            else:
                raise ValidationError(
                    {"error_message":
                     "There was a problem creating your request. "
                     "Please try again later."})

            # Get the formal address for the destination query
            destination_query = self.request.data.get('destination_query')
            destination = geolocator.geocode(destination_query, timeout=60)

            # There is a destination
            if destination and destination.latitude and destination.longitude:
                end_loc = (destination.latitude, destination.longitude)

                # The travel distance is <= to the max amount in settings
                if check_dist_between_start_end(start_loc, end_loc):
                    serializer.save(user=self.request.user,
                                    reservation_status=Reservation.PENDING,
                                    start_lat=start_loc[0],
                                    start_long=start_loc[1],
                                    destination_query=destination_query,
                                    end_long=destination.longitude,
                                    end_lat=destination.latitude)

                # Travel distance is too far
                else:
                    raise ValidationError(
                        {"error_message":
                         "Your destination is too far away. "
                         "Please choose somewhere closer."})

            # Cannot find the destination
            else:
                raise ValidationError(
                    {"error_message":
                     "Your destination cannot be found. "
                     "Please try another location nearby."})

        # The user has not confirmed his/her account
        else:
            raise ValidationError(
                {"error_message":
                 "Please confirm your account before continuing. "
                 "You should have received an email from us."})


class ReservationListAPIView(CacheMixin, DefaultsMixin, FiltersMixin,
                             generics.ListAPIView):
    cache_timeout = 60 * 60 * 24
    pagination_class = ReservationPagination
    serializer_class = ReservationSerializer
    search_fields = ('user__email, user__get_full_name',)
    ordering_fields = ('created', 'modified',)

    def get_queryset(self):
        user = self.request.user

        try:
            driver_res = Reservation.objects.get(
                Q(driver=user) & Q(reservation_status=Reservation.ACCEPTED))
        except:
            driver_res = None

        if driver_res:
            queryset = Reservation.objects.own_driver(user)
        else:
            queryset = Reservation.objects.pending().select_related(
                'user', 'driver')

        return queryset


class ReservationDetailAPIView(CacheMixin,
                               generics.RetrieveAPIView,
                               mixins.DestroyModelMixin,
                               mixins.UpdateModelMixin):
    cache_timeout = 60 * 7
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    serializer_class = ReservationSerializer

    def get_object(self):
        reservation_id = self.kwargs["reservation_id"]
        obj = get_object_or_404(Reservation, id=reservation_id)
        if obj.pick_up_interval < datetime.now().time():
            obj.reservation_status = Reservation.CANCELED
            obj.save()
        return obj

    def delete(self, request, *args, **kwargs):
        reservation_id = self.kwargs["reservation_id"]
        obj = get_object_or_404(Reservation, id=reservation_id)
        if request.user == obj.user:
            return self.destroy(request, *args, **kwargs)
        raise PermissionDenied(
            {"message": "You don't have permission to access this"})

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


# class ReservationDriversListAPIView(CacheMixin, DefaultsMixin, FiltersMixin,
#                                     generics.ListAPIView):
#     cache_timeout = 60
#     serializer_class = ReservationSerializer
#     search_fields = ('user__email, user__get_full_name',)
#     ordering_fields = ('created', 'modified',)

#     def get_queryset(self):
#         user = self.request.user

#         queryset = Reservation.objects.get(
#             user=user, reservation_status=Reservation.PENDING) \
#             .values('pending_drivers')
#         return queryset

#     def list(self, request):
#         queryset = self.get_queryset()
#         serializer = ReservationSerializer(queryset, many=True)
#         return RestResponse({serializer.data})


@api_view(['POST'])
def reservation_accept_api(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.pending_drivers.add(request.user)
    reservation.reservation_status = Reservation.SELECT
    reservation.save()
    serializer = ReservationSerializer(reservation,
                                       context={'request': request})
    return RestResponse(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def reservation_driver_found_api(request, reservation_id, driver_id):
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.driver = MyUser.objects.get(id=driver_id)
    reservation.reservation_status = Reservation.ACCEPTED
    reservation.save()
    serializer = ReservationSerializer(reservation,
                                       context={'request': request})
    return RestResponse(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def reservation_complete_api(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.reservation_status = Reservation.COMPLETED
    reservation.save()
    serializer = ReservationSerializer(reservation,
                                       context={'request': request})
    return RestResponse(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def reservation_cancel_api(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.reservation_status = Reservation.CANCELED
    reservation.save()
    serializer = ReservationSerializer(reservation,
                                       context={'request': request})
    return RestResponse(serializer.data, status=status.HTTP_201_CREATED)
