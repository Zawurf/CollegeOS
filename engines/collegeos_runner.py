from models.context import Context
from engines import ENGINES


def run_college_os(latitude, longitude):

    context = Context()

    context.location.latitude = latitude
    context.location.longitude = longitude

    for engine in ENGINES:
        engine.run(context)

    return context