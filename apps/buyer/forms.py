from django.forms import ModelForm
from core.models import UserProfile


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['tg_username', 'tg_notify_dlvr_create', 'tg_notify_dlvr_status',
                  'tg_is_connected', 'email_notify_dlvr_create', 'email_notify_dlvr_status']
