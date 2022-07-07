from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from scrapper.forms import AuthenticationFormWithBootstrapClasses
from .utils import WordreferenceScrapper
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import mimetypes

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


@method_decorator(login_required, name="dispatch")
class TranslationsPageView(TemplateView):
    template_name="scrapper/translations.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        context["random_list"] = range(1,100000)

        return context
    def post(self, request, *args, **kwargs):

        words = request.POST.getlist("words[]")
        options = {
            "principal-translation"  : bool(request.POST.get("principal-translation",False)),
            "additional-translation" : bool(request.POST.get("additional-translation",False)),
            "compound-form"          : bool(request.POST.get("compound-form",False)),
            "verbal-elocution"       : bool(request.POST.get("verbal-elocution",False))
        }
        deck_name = request.POST["deck_name"]
        
        wordreference_scrapper = WordreferenceScrapper(words, options, deck_name)
        
        file_absolute_url = wordreference_scrapper.start()
        
        path = open(file_absolute_url, 'rb')

        mime_type = mimetypes.guess_type(file_absolute_url)
        
        response = HttpResponse(path, content_type=mime_type)
        
        response['Content-Disposition'] = "attachment; filename=%s.apkg" % deck_name

        return response








