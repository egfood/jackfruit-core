from django import forms

from django.contrib.auth.password_validation import validate_password
from django.core import validators

from core.models import GreenUser


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    email = forms.EmailField(required=True, label="E-mail", widget=forms.EmailInput(attrs={'id': 'email'}),)
                             # validators=[validators.validate_email],
                             # error_messages={'invalid': 'Проверьте email'})
    password1 = forms.CharField(min_length=8, label="Пароль", widget=forms.PasswordInput(
                                attrs={'placeholder': 'Придумайте хороший пароль (минимум 8 символов)', 'id': 'password'}))
    password2 = forms.CharField(min_length=8, label="Подтверждение пароля",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Введите повторно пароль',
                                                                  'id': 'passwordRepeat'}))
    acceptConditions = forms.BooleanField(initial=True, widget=forms.CheckboxInput(attrs={'id': 'acceptConditions'}))

    class Meta:
        model = GreenUser
        fields = ("email", "password1", 'password2', 'acceptConditions')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            validate_password(password1)
        return password1

    def clean_password2(self):
        # super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Веденные пароли не совпадают!")
        return password2

    def save(self, commit=True):
        user = super().save()
        user.is_active = True
        user.is_activated = True
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
