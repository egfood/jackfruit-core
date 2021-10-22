from django import forms
from django.core import validators

from apps.farmer.models.profile import FarmerProfile


class FarmerSignupProfileForm(forms.ModelForm):
    name = forms.CharField(required=True, label='Имя', widget=forms.TextInput(attrs={"id": "profileName"}))
    phone = forms.CharField(required=True, label='Телефон',
                            widget=forms.TextInput(attrs={'placeholder': '+375 (xx) xxx-xx-xx ', "id": "profilePhone"}))
    region = forms.CharField(required=True, label='Населенный пункт (регион)',
                             widget=forms.TextInput(attrs={"id": "selectLocation"}))
    photo = forms.ImageField(required=False, validators=[validators.validate_image_file_extension],
                             widget=forms.ClearableFileInput(attrs={"style": 'display:none'}))

    class Meta:
        model = FarmerProfile
        fields = ('name', 'phone', 'region', 'photo')


class FarmerAreaProfileForm(forms.ModelForm):
    photo = forms.ImageField(required=False, validators=[validators.validate_image_file_extension],
                             widget=forms.ClearableFileInput(attrs={"style": 'display:none'}))
    name = forms.CharField(required=False, label='Имя', widget=forms.TextInput(attrs={"id": "profileName"}))
    phone = forms.CharField(required=False, label='Телефон',
                            widget=forms.TextInput(attrs={'placeholder': '+375 (xx) xxx-xx-xx ', "id": "profilePhone"}))
    region = forms.CharField(required=False, label='Населенный пункт (регион)',
                             widget=forms.TextInput(attrs={"id": "location"}))
    service_zone = forms.CharField(required=False, label='Зона обслуживания',
                                   widget=forms.TextInput(attrs={"id": "serviceZone"}))
    legal_name = forms.CharField(required=False, label='Название компании / фермерского хозяйства',
                                 widget=forms.TextInput(attrs={"id": "farmName"}))

    class Meta:
        model = FarmerProfile
        exclude = ('user',)
