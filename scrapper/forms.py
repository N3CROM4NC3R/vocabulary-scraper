from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from . import widgets
from django import forms

class AuthenticationFormWithBootstrapClasses(AuthenticationForm):
    
    username = forms.CharField(label='Email',widget = widgets.EmailInput)
    
    def __init__(self, *args, **kwargs):
        super(AuthenticationFormWithBootstrapClasses, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = 'form-control'
            visible.field.widget.label_classes = ('form-label',)
    
class TranslationForm(forms.Form):

    deck_name = forms.CharField(label = "deck_name", max_length = 50)

    principal_translations = forms.BooleanField(required = False)
    additional_translations = forms.BooleanField(required = False)
    compound_form = forms.BooleanField(required = False)
    verbal_locution = forms.BooleanField(required = False)

    def __init__(self, *args,**kwargs):
        super(TranslationForm, self).__init__(*args, **kwargs)

        words = self.data.get("words",dict())
        
        for i, word in enumerate(words):
            key = "word_%s" % i
            
            self.fields[key] = forms.CharField(required = True)
            
            self.data.update({key: word})

    def clean(self):
        words = set()
        
        i = 0
        
        field_name = 'word_%s' % (i,)
        
        while self.cleaned_data.get(field_name):
            word = self.cleaned_data[field_name]

            words.add(word)
            i += 1
            field_name = 'word_%s' % (i,)
       
        self.cleaned_data["words"] = words
