from django import forms
from .models import Photo


class NameForm(forms.Form):
    user_name = forms.CharField(label='User name', max_length=100)


class UploadPhotoForm(forms.ModelForm):
    """
    Form for uploading photo
    """

    def __init__(self, data=None, files=None, auto_id="id_%s", prefix=None, initial=None, error_class=None, label_suffix=None, empty_permitted=False, instance=None ):
        super(UploadPhotoForm, self).__init__(data=data, files=files, auto_id=auto_id, prefix=prefix, initial=initial, label_suffix=label_suffix, empty_permitted=empty_permitted, instance=instance)
        self.fields["preview"].label = u"Upload photo"

    class Meta:

        model = Photo
        fields = ["preview", ]

    def clean_preview(self):
        preview = self.cleaned_data.get('preview')

        if not preview:
            raise forms.ValidationError("Please upload photo.")
        return preview
