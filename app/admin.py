from django.contrib import admin
from .models import Utente, Corso, Fascia, Giorno

admin.site.register(Utente)
admin.site.register(Corso)
admin.site.register(Fascia)
admin.site.register(Giorno)
