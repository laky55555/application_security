from django.conf.urls import url

from . import views

app_name = 'hw5'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^ldap/', views.ldap, name='ldap'),
]
