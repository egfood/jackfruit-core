from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class ChildPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView, ):
    success_message = 'Ваш пароль успешно изменен. Используйте его для входа на сайт'
    success_url = reverse_lazy('login')
