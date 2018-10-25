from django.conf.urls import url
from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.home),
    url(r'^corsi/$', views.corsi),
    url(r'^mieicorsi/$', views.miei_corsi),
    path(r'iscriviti/<idcorso>', views.iscrizione),
    url(r'^home/$', views.home),
    url(r'^login/$', views.login_page),
    path(r'giorni/<giorno>', views.filtra_giorni),
    path(r'categorie/<categoria>', views.filtra_categorie),
    url(r'^creacorso/$', views.create_corso),
    url(r'^logout/$', views.logout_view),
    path(r'success/<idcorso>', views.success_view),
    path(r'rimuovi/<idcorso>', views.rimuovi_iscrizione),
    path(r'rimuovicorso/<idcorso>', views.rimuovi_corso),
    path(r'accetta/<idapprovazione>', views.accetta_corso),
    url(r'^newuser/$', views.create_user),
]
