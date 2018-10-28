import os
import sys
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SettimanaFlessibile.settings")

import django
django.setup()

from SettimanaFlessibile import setup
setup()

from app.models import Utente, Corso, Fascia
from app.methods import Corso_Delegate

studenti = Utente.objects.all()
totale = studenti.count()
fasce = Fascia.objects.all()
corsi = Corso.objects.all()

for counter, studente in enumerate(studenti):
    sys.stdout.write("\rProgress: {0}>".format("="*int((counter+1)/totale*20)))
    sys.stdout.flush()

    for f in fasce:
        if studente.is_fascia_taken(f) == False:
            print()
            #1) prova a iscrivere lo studente.
            #2) se non funziona, passa al prossimo corso finchè non trovi un corso funziona, allora: break


#check finale (implementa)

print()
print('Completed: {0} out of {0} students done'.format(totale))
