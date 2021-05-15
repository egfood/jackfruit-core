from django import forms
from django.core import validators

from core.models import UserProfile


class UserProfileForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['phone'].required = True
    REGION = (
        ('minsk', 'Минск'),
        ('minskRegion', 'Минская область')
    )
    # user_id = forms.NumberInput()
    tg_name = forms.CharField(required=True, label='Имя', widget=forms.TextInput(attrs={"id": "profileName"}))
    # phone = forms.RegexField(regex="\s{0,}\+{1,1}375\s{0,}\({0,1}(([2]{1}([5]{1}|[9]{1}))|([3]{1}[3]{1})|([4]{1}[4]{"
    #                                "1}))\)\s{0,}[0-9]{3,3}\s{0,}[0-9]{4,4}", required=True, label='Телефон',
    #                          widget=forms.TextInput(attrs={'placeholder': '+375 (xx) xxx-xx-xx ', "id": "profilePhone"}))
    phone = forms.CharField(required=True, label='Телефон',
                            widget=forms.TextInput(attrs={'placeholder': '+375 (xx) xxx-xx-xx ', "id": "profilePhone"}))
    region = forms.CharField(required=True, label='Населенный пункт (регион)',
                             widget=forms.Select(choices=REGION, attrs={"id": "selectLocation"}))
    photo = forms.ImageField(required=False, validators=[validators.validate_image_file_extension],
                             widget=forms.ClearableFileInput(attrs={"style": 'display:none'}))


    class Meta:
        model = UserProfile
        fields = ('tg_name', 'phone', 'region', 'photo')

    # def save(self, commit=True):
    #     user = super().save()
    #     user_id = .user.pk
    #     # user.(self.cleaned_data['password1'])
    #     if commit:
    #         user.save()
    #     return user
#   #     widgets = {
#         'tg_username': forms.TextInput(attrs={'placeholder': 'Username в Telegram без знака @'}),
#     }
