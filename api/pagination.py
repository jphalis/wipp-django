from rest_framework.pagination import LimitOffsetPagination


class AccountPagination(LimitOffsetPagination):
    default_limit = 15
    max_limit = 15
    limit_query_param = "limit"
    offset_query_param = "offset"


class ReservationPagination(LimitOffsetPagination):
    default_limit = 30
    max_limit = 50
    limit_query_param = "limit"
    offset_query_param = "offset"
