from django.core.cache import cache
from .models import Property


def get_all_properties():
    """
    Retrieve all properties from cache if available,
    otherwise fetch from database and cache for 1 hour
    """
    cached_properties = cache.get("all_properties")

    if cached_properties is not None:
        return cached_properties

    properties = Property.objects.all()
    cache.set("all_properties", properties, 3600)  # Cache for 1 hour (3600 seconds)
    return properties
