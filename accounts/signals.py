from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save)
def clear_cache(sender, instance=None, created=False, **kwargs):
    list_of_models = ('MyUser',)
    if sender.__name__ in list_of_models:
        if created:
            cache._cache.flush_all()
