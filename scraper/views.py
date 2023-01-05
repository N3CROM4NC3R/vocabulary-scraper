import json
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic.base import TemplateView, View
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout


from wordreference_scraper.wordreference_scraper import WordreferenceScraper
from scraper.forms import AuthenticationFormWithBootstrapClasses, TranslationForm
from .utils import VocabularyAnkiDeckCreator
from .decorators import anonymous_required

class LandingPageView(TemplateView):
    template_name = "scraper/pages/landing-page.html"

    @method_decorator(anonymous_required(redirect_url=reverse_lazy("scraper:translations")))
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        context["random_list"] = range(1,100000)

        return context

class LoginPageView(LoginView):
    template_name = "scraper/pages/login.html"
    next_page = reverse_lazy("scraper:translations")

    authentication_form = AuthenticationFormWithBootstrapClasses
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["random_list"] = range(1,100000)
        return context

@method_decorator(login_required, name="dispatch")
class TranslationsPageView(TemplateView):
    template_name="scraper/pages/translations.html"
    
    form_class = TranslationForm


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        context["random_list"] = range(1,100000)

        context["request"] = self.request

        context["form"] = self.form_class()

        return context
    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)

        translation_form = TranslationForm(data)

        
        translation_form.is_valid()

        cleaned_data = translation_form.cleaned_data
        options = {
            "principal-translation"  : cleaned_data["principal_translations"],
            "additional-translation" : cleaned_data["additional_translations"],
            "compound-form"          : cleaned_data["compound_form"],
            "verbal-elocution"       : cleaned_data["verbal_locution"]
        }

        deck_name = cleaned_data["deck_name"]
        words = cleaned_data["words"]

        
        wordreference_scraper = WordreferenceScraper(words)

        scraped_words = wordreference_scraper.start()

        vocabulary_anki_deck_creator = VocabularyAnkiDeckCreator(scraped_words,deck_name)

        deck_file = vocabulary_anki_deck_creator.create()

        url = deck_file["secure_url"]
        
        response_data = {
            'status' : "ok",
            'downloadUrl' : url,
            "name": deck_name,
        }

        response = JsonResponse(response_data)

        return response

def logout_view(request):
    logout(request)

    return redirect(reverse_lazy("scraper:landingPage"))




