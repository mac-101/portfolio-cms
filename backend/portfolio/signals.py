from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Portfolio
from .utils import unique_portfolio_slug


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_portfolio(sender, instance, created, **kwargs):
    if created:
        Portfolio.objects.create(
            owner=instance,
            name=instance.username,
            slug=unique_portfolio_slug(instance.username),
            email=instance.email,
        )