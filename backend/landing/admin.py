from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("created_at", "category", "short_message", "name", "email", "user", "is_read")
    list_filter = ("category", "is_read")
    list_editable = ("is_read",)
    search_fields = ("message", "name", "email")
    readonly_fields = ("created_at", "user")

    @admin.display(description="Message")
    def short_message(self, obj):
        return obj.message[:60]