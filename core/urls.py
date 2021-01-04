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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path
from django.conf.urls.static import static
from django.views.generic import RedirectView

from core.views import *

app_name = 'core'

urlpatterns = [
    path('core-admin/', admin.site.urls),
    path('farmer/', include('apps.farmer.urls', namespace='farmer')),
    path('buyer/', include('apps.buyer.urls', namespace='buyer')),

    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots_txt"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('forgot-password/', TemplateView.as_view(template_name='core/pages/forgot-password.html'),
         name='forgot_password'),

    re_path(r'^healthcheck/', include('health_check.urls')),
    path('summernote/', include('django_summernote.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
