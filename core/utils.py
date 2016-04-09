from geopy.distance import vincenty

from django.conf import settings


def jwt_response_payload_handler(token, user, request, *args, **kwargs):
    data = {
        "token": token,
        "user": "{}".format(user.id),
        "userid": user.id,
        "active": user.is_active
    }
    return data


def check_dist_between_start_end(start_loc, end_loc):
    return vincenty(start_loc, end_loc).miles <= settings.MAX_MILE_DISTANCE
