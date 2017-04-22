"""hw5 URL Configuration

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
from django.conf.urls.static import static
from django.conf import settings

app_name = 'hw5'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^read_local', views.read_local, name='read_local'),
    url(r'^read_central', views.read_central, name='read_central'),
    url(r'^encrypt_decrypt', views.encrypt_decrypt, name='encrypt_decrypt'),
    url(r'^authenticate_user', views.authenticate_user, name='authenticate_user'),
    url(r'^search_user', views.search_user, name='search_user'),
    url(r'^sniffer', views.sniffer, name='sniffer'),
]
