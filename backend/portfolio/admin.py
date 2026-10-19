from django.contrib import admin
from .models import Portfolio, Project, Resume, Service, SocialLink, Stack_Category, TechStack


@admin.register(Stack_Category)
class StackCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("portfolio", "uploaded_at")
    search_fields = ("portfolio__name", "portfolio__owner__username")


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