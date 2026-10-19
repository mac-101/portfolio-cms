from rest_framework import serializers

from portfolio.models import Portfolio, Project, Resume, Service, SocialLink, TechStack


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ["name", "slug", "bio", "profile_image", "location", "email"]


class ProjectSerializer(serializers.ModelSerializer):
    tech_stack = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
        allow_null=True,
    )

    class Meta:
        model = Project
        fields = ["title", "slug", "category", "description", "image", "tech_stack",
                  "github_url", "live_url", "featured", "created_at"]


class TechStackSerializer(serializers.ModelSerializer):
    icon_url = serializers.ReadOnlyField()
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
        allow_null=True,
    )

    class Meta:
        model = TechStack
        fields = ["name", "slug", "icon", "experience_level", "category", "icon_url"]


class ServiceSerializer(serializers.ModelSerializer):
    icon_url = serializers.ReadOnlyField()

    class Meta:
        model = Service
        fields = ["title", "description", "icon", "icon_url"]


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ["platform", "url", "label"]


class ResumeSerializer(serializers.ModelSerializer):
    file = serializers.FileField(read_only=True, use_url=True)

    class Meta:
        model = Resume
        fields = ["file", "original_filename", "uploaded_at"]