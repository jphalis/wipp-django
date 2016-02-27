"""wipp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework_jwt import views as rest_framework_jwt_views

from . import views


admin.site.site_header = "Wipp Administration"


urlpatterns = [
    # Admin
    url(r'^hidden/secure/wipp/admin/', admin.site.urls),

    # API
    url(r'^hidden/secure/wipp/api/', include('api.urls')),
    url(r'^hidden/secure/wipp/auth/', include('rest_framework.urls',
        namespace='rest_framework')),
    url(r'^hidden/secure/wipp/api/auth/token/$',
        rest_framework_jwt_views.obtain_jwt_token,
        name='auth_login_api'),

    # General
    url(r'^$', views.home, name='home'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += [] + static(settings.STATIC_URL,
                               document_root=settings.STATIC_ROOT)
    urlpatterns += [] + static(settings.MEDIA_URL,
                               document_root=settings.MEDIA_ROOT)
