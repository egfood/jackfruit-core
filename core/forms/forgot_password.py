from django.contrib.auth.forms import PasswordResetForm
from django import forms


class ChildPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auto_id = "%s"
        self.label_suffix = ''

    email = forms.EmailField(
        label=("E-mail"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
