import logging

from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)

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


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache metrics
    Returns dictionary with:
    - hits: Total cache hits
    - misses: Total cache misses
    - hit_ratio: Cache hit ratio (0.0 to 1.0)
    - status: "healthy" if hit_ratio > 0.7, "needs_attention" otherwise
    """
    try:
        # Get Redis connection
        conn = get_redis_connection("default")

        # Get Redis INFO command output
        info = conn.info()

        # Extract cache stats
        hits = int(info["stats"]["keyspace_hits"])
        misses = int(info["stats"]["keyspace_misses"])

        # Calculate hit ratio (handle division by zero)
        total = hits + misses
        hit_ratio = hits / total if total > 0 else 0.0

        # Determine status
        status = "healthy" if hit_ratio > 0.7 else "needs_attention"

        # Prepare metrics dictionary
        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 4),
            "status": status,
            "total_operations": total,
        }

        # Log the metrics
        logger.info(
            "Redis cache metrics - Hits: %s, Misses: %s, Ratio: %.2f%%, Status: %s",
            hits,
            misses,
            hit_ratio * 100,
            status,
        )

        return metrics

    except Exception as e:
        logger.error("Failed to get Redis cache metrics: %s", str(e))
        return {"error": str(e), "status": "unavailable"}
