from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try to get data from Redis
    properties = cache.get('all_properties')

    if properties is None:
        # If not found in cache, query DB
        properties = list(Property.objects.all().values(
            "id", "title", "description", "price", "location"
        ))
        # Store in cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)

    return properties

