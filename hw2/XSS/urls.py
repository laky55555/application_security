from django.conf.urls import url

from . import views

app_name = 'XSS'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^reflected', views.reflected, name='reflected'),
    url(r'^stored', views.stored, name='stored'),
    url(r'^dom', views.dom, name='dom'),
    url(r'^protection-header', views.x_xss_protection_header, name='x_xss_protection_header'),
]
