"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView
from django.urls import path, re_path

from core.forms.forgot_password import ChildPasswordResetForm
from core.views import *

app_name = 'core'

urlpatterns = [
                  path('', HomeView.as_view(), name='home'),
                  path('core-admin/', admin.site.urls, name='admin'),
                  path('farmer/', include('apps.farmer.urls', namespace='farmer')),
                  path('buyer/', include('apps.buyer.urls', namespace='buyer')),
                  path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
                       name="robots_txt"),
                  path('login/', CustomLoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  # path('forgot-password/', TemplateView.as_view(template_name='core/pages/forgot-password.html'),
                  #      name='forgot_password'),
                  path('forgot-password/', PasswordResetView.as_view(template_name='core/pages/forgot-password.html',
                                                                     form_class=ChildPasswordResetForm,
                                                                     # extra_email_context={'protocol': 'https', 'domain': 'localhost:8055/'}
                                                                     ), name='forgot_password'),
                  path('forgot-password/done/',
                       PasswordResetDoneView.as_view(template_name='core/pages/password_send_email.html'),
                       name='password_reset_done'),
                  path('password-reset/<uidb64>/<token>/',
                       ChildPasswordResetConfirmView.as_view(template_name='core/pages/confirm_password.html'),
                       name='password_reset_confirm'),

                  re_path(r'^healthcheck/', include('health_check.urls')),
                  path('summernote/', include('django_summernote.urls')),
              ] + static(str(settings.VERSION), document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
