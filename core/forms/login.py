from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

import settings


class AuthenticationUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auto_id = "%s"
        self.label_suffix = ''
        self.use_required_attribute = False
    username = UsernameField(required=True, label='E-mail', widget=forms.EmailInput(
                            attrs={'autofocus': True, 'placeholder': 'Введите Email', 'id': 'email'}))
    captcha = ReCaptchaField(widget=ReCaptchaV3, label='')

    # ReCaptchaField fix for correct validation forever in local development
    if getattr(settings, 'DEBUG', False):
        captcha.clean = lambda x: True


