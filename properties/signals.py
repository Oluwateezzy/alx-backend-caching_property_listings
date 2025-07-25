from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Property


@receiver(post_save, sender=Property)
def invalidate_property_cache_on_save(sender, instance, **kwargs):
    """
    Invalidate cache when a Property is saved (created or updated)
    """
    cache.delete("all_properties")


@receiver(post_delete, sender=Property)
def invalidate_property_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate cache when a Property is deleted
    """
    cache.delete("all_properties")
