from django.conf import settings
from django.db import models


class Feedback(models.Model):
    class Category(models.TextChoices):
        GENERAL = "general", "General feedback"
        BUG = "bug", "Bug"
        FEATURE = "feature", "Feature request"
        CATALOG = "catalog", "V2 catalog idea"
        CONTACT = "contact", "Contact / support"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name="feedback",
    )
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.GENERAL)
    message = models.TextField(max_length=2000)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "feedback"

    def __str__(self):
        return f"{self.get_category_display()}: {self.message[:40]}"