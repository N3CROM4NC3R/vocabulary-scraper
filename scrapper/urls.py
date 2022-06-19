from django.urls import path
from . import views


app_name="scrapper"

urlpatterns=[
    path("", views.LandingPageView.as_view(), name="landingPage"),
]




