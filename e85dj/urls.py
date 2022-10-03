"""e85dj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static

from accounts import urls
from batchfund import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', include('home.urls')),
    re_path(r'accounts/', include(('accounts.urls','accounts'),namespace='accounts')),
    re_path(r'batchfund/', include(('batchfund.urls','batchfund'),namespace='batchfund')),
    re_path(r'paddyprj/', include(('paddyprj.urls','paddyprj'),namespace='paddyprj')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
