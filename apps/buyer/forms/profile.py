from django import forms
from django.core import validators

from ..models.profile import BuyerProfile


class BuyerSignupProfileForm(forms.ModelForm):
    name = forms.CharField(required=True, label='Имя', widget=forms.TextInput(attrs={"id": "profileName"}))
    phone = forms.CharField(required=True, label='Телефон',
                            widget=forms.TextInput(attrs={'placeholder': '+375 (xx) xxx-xx-xx ', "id": "profilePhone"}))
    region = forms.CharField(required=True, label='Населенный пункт (регион)',
                             widget=forms.TextInput(attrs={"id": "selectLocation"}))
    photo = forms.ImageField(required=False, validators=[validators.validate_image_file_extension],
                             widget=forms.ClearableFileInput(attrs={"style": 'display:none'}))

    class Meta:
        model = BuyerProfile
        fields = ('name', 'phone', 'region', 'photo')


class BuyerAreaProfileForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        exclude = ('user', 'region', 'date_creation', 'date_updated')
