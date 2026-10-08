from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", include("portfolio.urls")),
    path("", include("accounts.urls")),
    path("", RedirectView.as_view(pattern_name="dashboard_home", permanent=False)),
]