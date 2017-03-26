from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'bank'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^accounts/profile/$', views.profile, name='index'),
    url(r'^statinfo/$', views.stat_info),
    url(r'^mainmenu/$', views.mainmenu),
    url(r'^hacker/', views.hacker),
    url(r'^spend/', csrf_exempt(views.spend), name='spend'),

]
