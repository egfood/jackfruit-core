from django import forms
from django.contrib.auth.password_validation import validate_password

from core.models import GreenUser


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(
        attrs={'placeholder': 'Придумайте хороший пароль (минимум 8 символов)'}))
    password2 = forms.CharField(label="Подтверждение пароля",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Введите повторно пароль'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True

    class Meta:
        model = GreenUser
        fields = ("email", "first_name")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Веденные пароли не совпадают!")
        return password2

    def clean(self):
        cleaned_data = super().clean()
        validate_password(self.cleaned_data["password1"])
        return cleaned_data
