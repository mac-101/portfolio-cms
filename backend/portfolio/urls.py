from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_home, name="dashboard_home"),

    path("projects/", views.project_list, name="project_list"),
    path("projects/new/", views.ProjectCreate.as_view(), name="project_create"),
    path("projects/<int:pk>/edit/", views.ProjectUpdate.as_view(), name="project_update"),
    path("projects/<int:pk>/delete/", views.ProjectDelete.as_view(), name="project_delete"),
    path("projects/<int:pk>/", views.ProjectDetail.as_view(), name="project_detail"),
    path("projects/<int:pk>/toggle/<slug:field>/", views.project_toggle, name="project_toggle"),

    path("tech-stack/", views.tech_list, name="tech_list"),
    path("tech-stack/new/", views.TechCreate.as_view(), name="tech_create"),
    path("tech-stack/<int:pk>/edit/", views.TechUpdate.as_view(), name="tech_update"),
    path("tech-stack/<int:pk>/delete/", views.TechDelete.as_view(), name="tech_delete"),

    path("services/", views.service_list, name="service_list"),
    path("services/new/", views.ServiceCreate.as_view(), name="service_create"),
    path("services/<int:pk>/edit/", views.ServiceUpdate.as_view(), name="service_update"),
    path("services/<int:pk>/delete/", views.ServiceDelete.as_view(), name="service_delete"),

    path("socials/", views.social_list, name="social_list"),
    path("socials/new/", views.SocialCreate.as_view(), name="social_create"),
    path("socials/<int:pk>/edit/", views.SocialUpdate.as_view(), name="social_update"),
    path("socials/<int:pk>/delete/", views.SocialDelete.as_view(), name="social_delete"),

    path("settings/", views.settings_view, name="settings"),
    path("api/", views.api_info, name="api_info"),
]