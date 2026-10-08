from django.contrib import admin
from .models import Portfolio, TechStack, Project, Service, SocialLink


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "owner", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug", "owner__username")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "portfolio", "featured", "published", "created_at")
    list_filter = ("published", "featured", "portfolio")
    search_fields = ("title", "portfolio__name")
    filter_horizontal = ("tech_stack",)


@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ("name", "portfolio")
    list_filter = ("portfolio",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "portfolio")
    list_filter = ("portfolio",)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "portfolio")
    list_filter = ("portfolio",)