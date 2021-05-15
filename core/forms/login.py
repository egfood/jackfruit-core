from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms


class AuthenticationUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auto_id = "%s"
        self.label_suffix = ''
        self.use_required_attribute = False

    username = UsernameField(required=True, label='E-mail', widget=forms.EmailInput(
                            attrs={'autofocus': True, 'placeholder': 'Введите Email', 'id': 'email'}))


