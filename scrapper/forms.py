from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms



class AuthenticationFormWithBootstrapClasses(AuthenticationForm):
    
    username = forms.CharField(label='Email')
    
    def __init__(self, *args, **kwargs):
        super(AuthenticationFormWithBootstrapClasses, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = 'form-control'
            visible.field.widget.label_classes = ('form-label',)
    