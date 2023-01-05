from django.urls import path
from . import views

app_name="scraper"

urlpatterns=[
    path("", views.LandingPageView.as_view(), name="landingPage"),
    path("login", views.LoginPageView.as_view(redirect_authenticated_user=True), name="login"),
    path("translations", views.TranslationsPageView.as_view(), name="translations"),
    path("logout",view=views.logout_view,name="logout")
]




