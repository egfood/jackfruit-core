from django import forms

from core.models import UserProfile


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].required = True

    class Meta:
        model = UserProfile
        fields = ('phone', 'tg_username')

    widgets = {
        'tg_username': forms.TextInput(attrs={'placeholder': 'Username в Telegram без знака @'}),
    }
