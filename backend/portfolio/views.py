import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from .forms import (
    PortfolioForm,
    ProjectForm,
    ServiceForm,
    SocialLinkForm,
    TechStackForm,
)
from .models import Project, Service, SocialLink, TechStack

def api_base(request, portfolio):
    return request.build_absolute_uri(f"/api/public/portfolios/{portfolio.slug}/")


@login_required
def dashboard_home(request):
    portfolio = request.user.portfolio
    projects = portfolio.projects.all()

    n_projects = projects.count()
    n_tech = portfolio.tech_stack.count()
    n_services = portfolio.services.count()
    n_socials = portfolio.social_links.count()

    stats = [
        ("Projects", n_projects, "/dashboard/projects/"),
        ("Tech Stack", n_tech, "/dashboard/tech-stack/"),
        ("Services", n_services, "/dashboard/services/"),
        ("Social Links", n_socials, "/dashboard/socials/"),
    ]
    checklist = [
        ("Add a bio", bool(portfolio.bio)),
        ("Publish a project", projects.filter(published=True).exists()),
        ("Add your tech stack", n_tech > 0),
        ("Add a service", n_services > 0),
        ("Add a social link", n_socials > 0),
    ]

    return render(request, "dashboard/home.html", {
        "portfolio": portfolio,
        "stats": stats,
        "checklist": checklist,
        "done_count": sum(1 for _, done in checklist if done),
        "recent_projects": projects.prefetch_related("tech_stack")[:5],
        "api_url": api_base(request, portfolio),
    })


@login_required
def project_list(request):
    projects = request.user.portfolio.projects.prefetch_related("tech_stack")
    return render(request, "dashboard/projects.html", {"projects": projects})


@login_required
def tech_list(request):
    return render(request, "dashboard/tech_stack.html", {
        "items": request.user.portfolio.tech_stack.all()
    })


@login_required
def service_list(request):
    return render(request, "dashboard/services.html", {
        "items": request.user.portfolio.services.all()
    })


@login_required
def social_list(request):
    return render(request, "dashboard/socials.html", {
        "items": request.user.portfolio.social_links.all()
    })


@login_required
def settings_view(request):
    portfolio = request.user.portfolio
    form = PortfolioForm(request.POST or None, request.FILES or None, instance=portfolio)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Settings saved.")
        return redirect("settings")
    return render(request, "dashboard/settings.html", {"form": form, "portfolio": portfolio})

def build_endpoints(base, portfolio):
    project = {
        "title": "EchoNote",
        "slug": "echonote",
        "description": "A Django notes application.",
        "image": "https://res.cloudinary.com/your-cloud/image/upload/echonote.jpg",
        "tech_stack": ["Python", "Django"],
        "github_url": "https://github.com/you/echonote",
        "live_url": "https://echonote.example.com",
        "featured": True,
        "created_at": "2026-10-08T21:14:03Z",
    }

    def listing(item):
        return {"count": 1, "next": None, "previous": None, "results": [item]}

    endpoints = [
        {
            "title": "Portfolio",
            "path": "",
            "description": "Your public profile details.",
            "example": {
                "name": portfolio.name,
                "slug": portfolio.slug,
                "bio": "Backend developer building APIs.",
                "profile_image": None,
                "location": "City, Country",
                "email": "you@example.com",
            },
        },
        {
            "title": "Projects",
            "path": "projects/",
            "description": "All published projects, newest first. Drafts are never included.",
            "params": "?featured=true  ·  ?page=2  ·  ?page_size=10",
            "example": listing(project),
        },
        {
            "title": "Project detail",
            "path": "projects/echonote/",
            "description": "One published project, looked up by its slug.",
            "example": project,
        },
        {
            "title": "Tech stack",
            "path": "tech-stack/",
            "description": "Your technologies, sorted by name.",
            "example": listing({"name": "Django", "slug": "django", "icon": ""}),
        },
        {
            "title": "Services",
            "path": "services/",
            "description": "The services you offer.",
            "example": listing({
                "title": "Web Development",
                "description": "Modern, responsive websites.",
                "icon": "",
            }),
        },
        {
            "title": "Social links",
            "path": "socials/",
            "description": "Links to your profiles.",
            "example": listing({
                "platform": "GitHub",
                "url": "https://github.com/you",
                "label": "",
            }),
        },
    ]

    for ep in endpoints:
        ep["url"] = base + ep["path"]
        ep["example_json"] = json.dumps(ep["example"], indent=2)
    return endpoints


@login_required
def api_info(request):
    portfolio = request.user.portfolio
    base = api_base(request, portfolio)
    return render(request, "dashboard/api.html", {
        "base_url": base,
        "endpoints": build_endpoints(base, portfolio),
    })
    
class PortfolioMixin(LoginRequiredMixin):
    """Only ever returns objects that belong to the logged-in user's portfolio."""

    label = ""      # "Project"
    section = ""    # "Projects"
    list_url = ""   # URL name of the list page

    def get_queryset(self):
        return self.model.objects.filter(portfolio=self.request.user.portfolio)

    def get_success_url(self):
        return reverse(self.list_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(label=self.label, section=self.section, list_url=reverse(self.list_url))
        return ctx


class SaveView(PortfolioMixin, SuccessMessageMixin):
    template_name = "dashboard/form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["portfolio"] = self.request.user.portfolio
        return kwargs

    def get_success_message(self, cleaned_data):
        return f"{self.label} saved."


class RemoveView(PortfolioMixin, SuccessMessageMixin):
    template_name = "dashboard/confirm_delete.html"

    def get_success_message(self, cleaned_data):
        return f"{self.label} deleted."


# Projects
class ProjectMeta:
    model = Project
    label, section, list_url = "Project", "Projects", "project_list"


class ProjectCreate(ProjectMeta, SaveView, CreateView):
    form_class = ProjectForm


class ProjectUpdate(ProjectMeta, SaveView, UpdateView):
    form_class = ProjectForm


class ProjectDelete(ProjectMeta, RemoveView, DeleteView):
    """Uses Django's default empty confirmation form."""


# Tech stack
class TechMeta:
    model = TechStack
    label, section, list_url = "Technology", "Tech Stack", "tech_list"


class TechCreate(TechMeta, SaveView, CreateView):
    form_class = TechStackForm


class TechUpdate(TechMeta, SaveView, UpdateView):
    form_class = TechStackForm


class TechDelete(TechMeta, RemoveView, DeleteView):
    """Uses Django's default empty confirmation form."""


# Services
class ServiceMeta:
    model = Service
    label, section, list_url = "Service", "Services", "service_list"


class ServiceCreate(ServiceMeta, SaveView, CreateView):
    form_class = ServiceForm


class ServiceDetail(ServiceMeta, PortfolioMixin, DetailView):
    template_name = "dashboard/service_detail.html"


class ServiceUpdate(ServiceMeta, SaveView, UpdateView):
    form_class = ServiceForm


class ServiceDelete(ServiceMeta, RemoveView, DeleteView):
    """Uses Django's default empty confirmation form."""


# Social links
class SocialMeta:
    model = SocialLink
    label, section, list_url = "Social link", "Socials", "social_list"


class SocialCreate(SocialMeta, SaveView, CreateView):
    form_class = SocialLinkForm


class SocialUpdate(SocialMeta, SaveView, UpdateView):
    form_class = SocialLinkForm


class SocialDelete(SocialMeta, RemoveView, DeleteView):
    """Uses Django's default empty confirmation form."""
    
# Projects
class ProjectMeta:
    model = Project
    label, section, list_url = "Project", "Projects", "project_list"


class ProjectRedirectMixin:
    """After saving, go to the project's detail page instead of the list."""

    def get_success_url(self):
        return reverse("project_detail", args=[self.object.pk])


class ProjectCreate(ProjectRedirectMixin, ProjectMeta, SaveView, CreateView):
    form_class = ProjectForm


class ProjectUpdate(ProjectRedirectMixin, ProjectMeta, SaveView, UpdateView):
    form_class = ProjectForm


class ProjectDelete(ProjectMeta, RemoveView, DeleteView):
    """Uses Django's default empty confirmation form."""


class ProjectDetail(ProjectMeta, PortfolioMixin, DetailView):
    template_name = "dashboard/project_detail.html"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("tech_stack")


@login_required
@require_POST
def project_toggle(request, pk, field):
    if field not in ("published", "featured"):
        raise Http404
    project = get_object_or_404(Project, pk=pk, portfolio=request.user.portfolio)
    setattr(project, field, not getattr(project, field))
    project.save(update_fields=[field, "updated_at"])
    state = "on" if getattr(project, field) else "off"
    messages.success(request, f"{field.capitalize()} turned {state}.")
    return redirect("project_detail", pk=project.pk)