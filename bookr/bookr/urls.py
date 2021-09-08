"""bookr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from bookr.views import profile
from bookr_admin.admin import admin_site

urlpatterns = [
    # `include()` is a shortcut that allows you to combine URL configurations.
    # It is common to keep one URL configuration per application in your Django project.
    # Here, we've created a separate URL configuration for the `reviews` app and have
    # added it to our project-level URL configuration.
    # TODO Why does the `admin/` path not use `include()`? It doesn't follow any of the
    # pattern found in the examples (see docstring on top of this file).
    # TODO POSSIBLE ANSWER: admin.site.urls is already a tuple
    path("", include('reviews.urls')),
    path("admin/", admin_site.urls),
    path(
        "accounts/", include(('django.contrib.auth.urls', 'auth'), namespace='accounts')
    ),
    path("accounts/profile/", profile, name="profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
