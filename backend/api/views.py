from django.shortcuts import get_object_or_404
from rest_framework import generics

from portfolio.models import Portfolio, Project, Service, SocialLink, TechStack

from .serializers import (
    PortfolioSerializer, ProjectSerializer, ServiceSerializer,
    SocialLinkSerializer, TechStackSerializer,
)


class PortfolioScopedMixin:
    """Finds the portfolio from the URL slug, or returns 404."""

    def get_portfolio(self):
        if not hasattr(self, "_portfolio"):
            self._portfolio = get_object_or_404(Portfolio, slug=self.kwargs["slug"])
        return self._portfolio


class PortfolioDetail(generics.RetrieveAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    lookup_field = "slug"


class ProjectList(PortfolioScopedMixin, generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        qs = (
            Project.objects.filter(portfolio=self.get_portfolio(), published=True)
            .prefetch_related("tech_stack")
        )
        featured = self.request.query_params.get("featured")
        if featured is not None:
            qs = qs.filter(featured=featured.lower() in ("1", "true", "yes"))
        return qs


class ProjectDetail(PortfolioScopedMixin, generics.RetrieveAPIView):
    serializer_class = ProjectSerializer

    def get_object(self):
        qs = Project.objects.filter(
            portfolio=self.get_portfolio(), published=True
        ).prefetch_related("tech_stack")
        return get_object_or_404(qs, slug=self.kwargs["project_slug"])


class TechStackList(PortfolioScopedMixin, generics.ListAPIView):
    serializer_class = TechStackSerializer

    def get_queryset(self):
        return TechStack.objects.filter(portfolio=self.get_portfolio())


class ServiceList(PortfolioScopedMixin, generics.ListAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.filter(portfolio=self.get_portfolio()).order_by("id")


class SocialLinkList(PortfolioScopedMixin, generics.ListAPIView):
    serializer_class = SocialLinkSerializer

    def get_queryset(self):
        return SocialLink.objects.filter(portfolio=self.get_portfolio()).order_by("id")