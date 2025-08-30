from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

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

def get_redis_cache_metrics():
    """
    Retrieve Redis cache metrics: hits, misses, and hit ratio.
    """
    conn = get_redis_connection("default")
    info = conn.info()

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total_requests = hits + misses

    try:
        hit_ratio = hits / total_requests if total_requests > 0 else 0
    except Exception as e:
        logger.error(f"Error calculating hit ratio: {e}")
        hit_ratio = 0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2),
    }

    logger.info(f"Redis Cache Metrics: {metrics}")
    return metrics

