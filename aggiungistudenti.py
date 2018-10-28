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
