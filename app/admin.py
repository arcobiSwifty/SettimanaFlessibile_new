from django.contrib import admin
from .models import Utente, Corso, Fascia, Giorno, Aula, Approvazione, Categoria

admin.site.register(Utente)
admin.site.register(Corso)
admin.site.register(Fascia)
admin.site.register(Giorno)
admin.site.register(Aula)
admin.site.register(Approvazione)
admin.site.register(Categoria)
