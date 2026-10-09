from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="landing_home"),
    path("feedback/", views.feedback, name="feedback"),
    path("feedback/thanks/", views.feedback_thanks, name="feedback_thanks"),
]