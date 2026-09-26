from geopy.distance import geodesic
from config import COLLEGE_LOCATION, CAMPUS_RADIUS


def distance_from_college(location):
    return round(geodesic(location, COLLEGE_LOCATION).meters, 2)


def is_inside_campus(location):
    return distance_from_college(location) <= CAMPUS_RADIUS


def get_current_zone(inside_campus):
    return "Campus" if inside_campus else "Outside"



def run(context):

    latitude = context.location.latitude
    longitude = context.location.longitude

    if latitude is None or longitude is None:
        return context

    location = (latitude, longitude)

    distance = distance_from_college(location)
    inside = is_inside_campus(location)
    zone = get_current_zone(inside)

    context.location.distance_from_college = distance
    context.location.inside_campus = inside
    context.location.zone = zone

    return context