from django.conf.urls import url
from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.home),
    url(r'^corsi/$', views.corsi),
    path(r'iscriviti/<idcorso>', views.iscrizione),
    url(r'^home/$', views.home),
    url(r'^login/$', views.login_page),
    url(r'^newuser/$', views.create_user),
    url(r'^creacorso/$', views.create_corso),
]
