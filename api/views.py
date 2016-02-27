from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from rest_framework import generics, mixins, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response as RestResponse
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from accounts.models import MyUser
from core.mixins import AdminRequiredMixin, CacheMixin
from reservations.models import Reservation
from .account_serializers import AccountCreateSerializer, MyUserSerializer
from .auth_serializers import (PasswordResetSerializer,
                               PasswordResetConfirmSerializer,
                               PasswordChangeSerializer)
from .mixins import DefaultsMixin, FiltersMixin
from .pagination import AccountPagination, ReservationPagination
from .permissions import IsOwnerOrReadOnly, MyUserIsOwnerOrReadOnly
from .reservation_serializers import ReservationSerializer

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
                'edit_profile_url': api_reverse(
                    'user_account_detail_api', request=request,
                    kwargs={'username': request.user.username})
            },
            'reservations': {
                'count': Reservation.objects.all().count(),
                'url': api_reverse('reservation_list_api', request=request),
                # 'create_url': api_reverse('reservation_create_api',
                #                           request=request),
            },
        }
        return RestResponse(data)


# A C C O U N T S
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
        username = self.kwargs["username"]
        obj = get_object_or_404(MyUser, username=username)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


# A U T H E N T I C A T I O N
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


# R E S E R V A T I O N S
# class ReservationCreateAPIView(ModelViewSet):
#     queryset = Reservation.objects.select_related('creator').all()
#     serializer_class = ReservationCreateSerializer
#     parser_classes = (MultiPartParser, FormParser,)

#     def perform_create(self, serializer):
#         user = self.request.user
#         user.save()
#         serializer.save(creator=user,
#                         slug=get_random_string(length=10),
#                         photo=self.request.data.get('photo'))


class ReservationListAPIView(CacheMixin, DefaultsMixin, FiltersMixin,
                             generics.ListAPIView):
    cache_timeout = 60 * 60 * 24
    pagination_class = ReservationPagination
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.select_related('user', 'driver')
    search_fields = ('user__username',)
    ordering_fields = ('created', 'modified',)


# class ReservationDetailAPIView(CacheMixin,
#                                generics.RetrieveAPIView,
#                                mixins.DestroyModelMixin,
#                                mixins.UpdateModelMixin):
#     cache_timeout = 60 * 7
#     permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
#     serializer_class = ReservationSerializer

#     def get_object(self):
#         cat_slug = self.kwargs["cat_slug"]
#         photo_slug = self.kwargs["photo_slug"]
#         category = get_object_or_404(Category, slug=cat_slug)
#         obj = get_object_or_404(Photo, category=category, slug=photo_slug)
#         return obj

#     def delete(self, request, *args, **kwargs):
#         cat_slug = self.kwargs["cat_slug"]
#         photo_slug = self.kwargs["photo_slug"]
#         category = get_object_or_404(Category, slug=cat_slug)
#         obj = get_object_or_404(Photo, category=category, slug=photo_slug)
#         if request.user == obj.creator:
#             return self.destroy(request, *args, **kwargs)
#         raise PermissionDenied(
#             {"message": "You don't have permission to access this"})

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
