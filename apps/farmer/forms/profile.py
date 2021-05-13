from django import forms
from django.core import validators

from apps.farmer.models import FarmerProfile


class FarmerProfileForm(forms.ModelForm):
    REGION = (
        ('minsk', 'Минск'),
        ('minskRegion', 'Минская область')
    )
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
