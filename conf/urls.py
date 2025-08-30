from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogs.urls')),
    path("favicon.ico", RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    path("logo.png", RedirectView.as_view(url='/static/logo.png', permanent=True)),
    path("apple-touch-icon.png", RedirectView.as_view(url='/static/logo.png', permanent=True)),
    path("apple-touch-icon-precomposed.png", RedirectView.as_view(url='/static/logo.png', permanent=True)),
    re_path(r"^favicons/.*$", RedirectView.as_view(url='/static/logo.png', permanent=True)),
]

# Debug toolbar removed - no longer needed for personal CMS

handler404 = 'blogs.views.blog.not_found'
