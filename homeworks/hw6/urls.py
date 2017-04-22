"""hw6 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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

from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'hw6'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^captcha$', views.captcha, name='captcha'),
    url(r'^s_key$', views.s_key, name='s_key'),
    url(r'^s_key_generate$', views.s_key_generate, name='s_key_generate'),
    url(r'^logout$', auth_views.logout, {'next_page' : '/hw6/s_key'}),
    url(r'^s_key', auth_views.login, name='s_key'),
]
