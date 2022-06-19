from django.shortcuts import render
from django.views.generic.base import TemplateView

class LandingPageView(TemplateView):
    template_name = "scrapper/landing-page.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        context["random_list"] = range(1,100000)

        return context



# Create your views here.
