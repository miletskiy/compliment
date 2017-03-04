from django import forms

class NameForm(forms.Form):
    user_name = forms.CharField(label='User name', max_length=100)