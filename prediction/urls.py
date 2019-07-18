"""prediction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from global_login_required import login_not_required

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView



urlpatterns = [
    url(r'^admin/', admin.site.urls),
]


urlpatterns += [
    url(r'^predict/', include('prediction_app.urls')),
    url(r'^accounts/login/$', login_not_required(RedirectView.as_view(url='/predict/login', permanent=False)), name='redirect_url')

]
