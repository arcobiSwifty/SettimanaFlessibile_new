from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^iscrizione/$', views.iscrizione),
    url(r'^home/$', views.home),
    url(r'^login/$', views.login_page),
    url(r'^newuser/$', views.create_user),
]
