from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from scrapper.forms import AuthenticationFormWithBootstrapClasses



class LandingPageView(TemplateView):
    template_name = "scrapper/landing-page.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        context["random_list"] = range(1,100000)

        return context

class LoginPageView(LoginView):
    template_name = "scrapper/login.html"
    #next_page = reverse("scrapper:landing-page")

    authentication_form = AuthenticationFormWithBootstrapClasses


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["random_list"] = range(1,100000)
        return context


