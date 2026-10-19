from django.urls import path

from . import views

urlpatterns = [
    path("portfolios/<slug:slug>/", views.PortfolioDetail.as_view()),
    path("portfolios/<slug:slug>/projects/", views.ProjectList.as_view()),
    path("portfolios/<slug:slug>/projects/<slug:project_slug>/", views.ProjectDetail.as_view()),
    path("portfolios/<slug:slug>/tech-stack/", views.TechStackList.as_view()),
    path("portfolios/<slug:slug>/services/", views.ServiceList.as_view()),
    path("portfolios/<slug:slug>/socials/", views.SocialLinkList.as_view()),
    path("portfolios/<slug:slug>/resume/", views.ResumeDetail.as_view(), name="public_resume"),
]