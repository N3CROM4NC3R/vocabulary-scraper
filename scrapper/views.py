from django.shortcuts import redirect
from django.urls import  reverse_lazy
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from scrapper.forms import AuthenticationFormWithBootstrapClasses
from .utils import WordreferenceScrapper
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout

import json

from .decorators import anonymous_required

class LandingPageView(TemplateView):
    template_name = "scrapper/landing-page.html"

    @method_decorator(anonymous_required(redirect_url=reverse_lazy("scrapper:translations")))
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        context["random_list"] = range(1,100000)

        return context


class LoginPageView(LoginView):
    template_name = "scrapper/login.html"
    next_page = reverse_lazy("scrapper:translations")

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

        context["request"] = self.request

        return context
    def post(self, request, *args, **kwargs):

        
        data = json.loads(request.body)
     
        options = {
            "principal-translation"  : bool(data.get("principal-translation",False)),
            "additional-translation" : bool(data.get("additional-translation",False)),
            "compound-form"          : bool(data.get("compound-form",False)),
            "verbal-elocution"       : bool(data.get("verbal-elocution",False))
        }
        deck_name = data["deck_name"]
        words = data["words"]
        
        wordreference_scrapper = WordreferenceScrapper(words, options, deck_name)
        
        file = wordreference_scrapper.start()

        url = file["secure_url"]
        
        response_data = {
            'status':"ok",
            'downloadUrl':url
        }

        response = JsonResponse(response_data)

        return response



def logout_view(request):
    logout(request)

    return redirect(reverse_lazy("scrapper:landingPage"))




