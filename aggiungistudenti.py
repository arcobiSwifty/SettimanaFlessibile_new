#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SettimanaFlessibile.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

from app.models import Utente, Corso
from django.contrib.auth.models import User

print('starting process')

utenti = Utente.objects.all()
total = utenti.count()

for counter, studente in enumerate(utenti):
    sys.stdout.write("\r{0}>".format("{0}/{1} -- {2}".format(counter, total, studente)))
    sys.stdout.flush()
