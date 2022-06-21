from django.forms.widgets import TextInput

class EmailInput(TextInput):
    input_type = 'email'