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
    """
    Checks to see if the distance between the starting location
    and ending location is less than the MAX_MILE_DISTANCE in the
    settings file.
    Returns True if less than or equal to. Returns False if greater than.
    """
    return vincenty(start_loc, end_loc).miles <= settings.MAX_MILE_DISTANCE
