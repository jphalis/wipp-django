import requests

from django.conf import settings


GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/'
GEOCODE_URL = GOOGLE_MAPS_API_URL + 'geocode/json?'
DISTANCE_MATRIX_URL = GOOGLE_MAPS_API_URL + \
    'distancematrix/json?units=imperial&'


def jwt_response_payload_handler(token, user, request, *args, **kwargs):
    data = {
        "token": token,
        "user": "{}".format(user.id),
        "userid": user.id,
        "active": user.is_active
    }
    return data


def travel_distance(start_lat, start_lng, end_lat, end_lng, validator=True):
    """
    Checks to see if the distance between the starting location
    and ending location is less than the MAX_MILE_DISTANCE in the
    settings file.
    Returns True if less than or equal to. Returns False if greater than.
    """
    api_response = requests.get(
        DISTANCE_MATRIX_URL + 'origins={0},{1}&destinations={2}%2c{3}&key={4}'.format(
            start_lat, start_lng, end_lat, end_lng, settings.GOOGLE_MAPS_KEY))
    api_response_dict = api_response.json()
    if api_response_dict['status'] == "OK":
        miles = api_response_dict['rows'][0]['elements'][0]['distance']['value'] * 0.000621371
        if validator:
            return miles <= settings.MAX_MILE_DISTANCE
        return "{0:.2f} mi".format(miles)
    return None


def verbose_address(latitude, longitude):
    """
    Returns the formatted address corresponding to a set of coordinates.
    """
    api_response = requests.get(
        GEOCODE_URL + 'latlng={0},{1}&key={2}'.format(
            latitude, longitude, settings.GOOGLE_MAPS_KEY))
    api_response_dict = api_response.json()
    if api_response_dict['status'] == "OK":
        return api_response_dict['results'][0]['formatted_address']
    return None


def address_from_query(query):
    """
    Returns the address formatted address of a query.
    """
    api_response = requests.get(
        GEOCODE_URL + 'address={0}&key={1}'.format(query,
                                                   settings.GOOGLE_MAPS_KEY))
    api_response_dict = api_response.json()
    if api_response_dict['status'] == "OK":
        return api_response_dict['results'][0]['formatted_address']
    return None


def coordinates_from_query(query):
    """
    Returns the coordinates from a query.
    """
    api_response = requests.get(
        GEOCODE_URL + 'address={0}&key={1}'.format(query,
                                                   settings.GOOGLE_MAPS_KEY))
    api_response_dict = api_response.json()
    if api_response_dict['status'] == "OK":
        lat = api_response_dict['results'][0]['geometry']['location']['lat']
        lng = api_response_dict['results'][0]['geometry']['location']['lng']
        return (lat, lng)
    return None
