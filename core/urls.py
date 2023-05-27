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
from django.urls import path

from apps.buyer.api import urls as buyer_urls
from apps.farmer.api import urls as farmer_urls
from apps.store.api import urls as store_urls
from core.forms.forgot_password import ChildPasswordResetForm
from core.views import *

app_name = 'core'

urlpatterns = [
                  path('', HomeView.as_view(), name='home'),
                  path('core-admin/', admin.site.urls, name='admin'),
                  path('farmer/', include('apps.farmer.urls', namespace='farmer')),
                  path('buyer/', include('apps.buyer.urls', namespace='buyer')),
                  path('store/', include('apps.store.urls', namespace='store')),
                  path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
                       name="robots_txt"),
                  path('login/', CustomLoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('forgot-password/', PasswordResetView.as_view(template_name='core/pages/forgot-password.html',
                                                                     form_class=ChildPasswordResetForm),
                       name='forgot_password'),
                  path('forgot-password/done/',
                       PasswordResetDoneView.as_view(template_name='core/pages/password_send_email.html'),
                       name='password_reset_done'),
                  path('password-reset/<uidb64>/<token>/',
                       ChildPasswordResetConfirmView.as_view(template_name='core/pages/confirm_password.html'),
                       name='password_reset_confirm'),

                  path('summernote/', include('django_summernote.urls')),
                  path('api/v1/farmer/', include(farmer_urls, namespace='farmer_api')),
                  path('api/v1/store/', include(store_urls, namespace='store_api')),
                  path('api/v1/buyer/', include(buyer_urls, namespace='buyer_api')),
              ] + static(str(settings.VERSION), document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
