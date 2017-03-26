from django.conf.urls import url

from . import views

app_name = 'rest'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^third/', views.third, name='third'),
    url(r'^fifth/', views.fifth, name='fifth'),
]
