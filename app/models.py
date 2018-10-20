from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MaxValueValidator, MinValueValidator

import json

class JSONField(models.TextField):

    def to_python(self, value):
        if value == "":
            return None

        try:
            if isinstance(value, str):
                return json.loads(value)
        except ValueError:
            pass
        return value

    def from_db_value(self, value, *args):
        return self.to_python(value)

    def get_db_prep_save(self, value, *args, **kwargs):
        if value == "":
            return None
        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)
        return value

class Aula(models.Model):
    nome_aula = models.CharField(
        max_length=100,
        choices=([
            ('Palestra', 'Palestra'),
            ('Aula Normale', 'Aula Normale'),
            ('Aula Magna', 'Aula Magna'),
            ('Laboratorio di informatica', 'Laboratorio di informatica'),
        ]),
    )
    capacita = models.IntegerField(default=30)

    def __str__(self):
        return self.nome_aula

class Giorno(models.Model):
    giorno_della_settimana = models.CharField(
        max_length=80,
        choices=([
            ('Lunedì', 'Lunedì'),
            ('Martedì', 'Martedì'),
            ('Mercoledì', 'Mercoledì'),
            ('Giovedì', 'Giovedì'),
            ('Venerdì', 'Venerdì'),
        ]),
        default='Lunedì'
    )

    def __str__(self):
        return self.giorno_della_settimana


class Fascia(models.Model):
    giorno = models.ForeignKey('Giorno', on_delete=models.CASCADE)
    fascia = models.CharField(
        max_length=80,
        choices=([
            ('Prima Fascia', 'Prima Fascia'),
            ('Seconda Fascia', 'Seconda Fascia'),
            ('Terza Fascia', 'Terza Fascia'),
        ]),
        default='Prima Fascia'
    )

    def __str__(self):
        return self.giorno.giorno_della_settimana + ', ' + self.fascia



class Corso(models.Model):

    nome = models.CharField(max_length=100)

    descrizione = models.TextField(max_length=1500)

    is_progressive = models.BooleanField(default=True)

    fasce = models.ManyToManyField('Fascia')

    aula = models.ForeignKey('Aula', on_delete=models.CASCADE, related_name='aula')

    creatore = models.ForeignKey('Utente', on_delete=models.CASCADE, related_name='creatore')

    ospitanti = models.ManyToManyField('Utente')

    iscritti = models.ManyToManyField('Utente', related_name='iscritti')

    def __str__(self):
        return self.nome



class Utente(models.Model):

    nome = models.CharField(max_length=150)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


    #should be corsi a cui è iscritto id
    iscrizioni = models.ManyToManyField('Corso', related_name='iscrizioni')

    classe = models.IntegerField(default=1,validators=[MaxValueValidator(5), MinValueValidator(1)])
    sezione = models.CharField(max_length=1)

    hosted_courses = models.ManyToManyField('Corso')

    def is_fascia_taken(self, fascia_to_check):
        iscrizione = Corso.objects.filter(iscritti__contains=self).filter(fasce__contains=fascia_to_check).count()
        if iscrizione > 0:
            return True
        return False

    def __str__(self):
        return self.nome
