from django import forms
from .models import Photo


class NameForm(forms.Form):
    user_name = forms.CharField(label='User name', max_length=100)


class UploadPhotoForm(forms.ModelForm):
    """
    Form for uploading photo
    """

    class Meta:
        model = Photo
        fields = ["title", "preview", ]

