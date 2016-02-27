from django.conf.urls import url


from . import views
from .views import APIHomeView
from .views import (AccountCreateAPIView,
                    MyUserDetailAPIView, MyUserListAPIView,
                    DriverDetailAPIView)
from .views import (PasswordChangeView, PasswordResetView,
                    PasswordResetConfirmView)
from .views import ReservationListAPIView


# app_name = 'api'
urlpatterns = [
    # G E N E R A L
    url(r'^$', APIHomeView.as_view(),
        name='api_home'),

    # A C C O U N T S
    url(r'^accounts/$', MyUserListAPIView.as_view(),
        name='user_account_list_api'),
    url(r'^accounts/create/$', AccountCreateAPIView.as_view(),
        name='account_create_api'),
    url(r'^accounts/(?P<id>\d+)/$', MyUserDetailAPIView.as_view(),
        name='user_account_detail_api'),
    url(r'^accounts/driver/(?P<id>\d+)/$', DriverDetailAPIView.as_view(),
        name='user_driver_detail_api'),

    # A U T H E N T I C A T I O N
    url(r'^password/reset/$', PasswordResetView.as_view(),
        name='rest_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(),
        name='rest_password_reset_confirm'),
    url(r'^password/change/$', PasswordChangeView.as_view(),
        name='rest_password_change'),

    # R E S E R V A T I O N S
    url(r'^reservations/$', ReservationListAPIView.as_view(),
        name='reservation_list_api'),
    # url(r'^reservations/create/$', ReservationCreateAPIView.as_view({'post': 'create'}),
    #     name='reservation_create_api'),
    # url(r'^reservations/(?P<reservation_pk>\d+)/$',
    #     ReservationDetailAPIView.as_view(), name='reservation_detail_api'),
]
