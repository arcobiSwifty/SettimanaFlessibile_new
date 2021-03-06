from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MaxValueValidator, MinValueValidator


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

class Categoria(models.Model):

    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome

class Corso(models.Model):

    nome = models.CharField(max_length=100)
    descrizione = models.TextField(max_length=1500)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, null=True, blank=True)

    is_progressive = models.BooleanField(default=True)
    fasce = models.ManyToManyField('Fascia')

    aula = models.ForeignKey('Aula', on_delete=models.CASCADE, related_name='aula')

    creatore = models.ForeignKey('Utente', on_delete=models.CASCADE, related_name='creatore')
    ospitanti = models.ManyToManyField('Utente')

    iscritti = models.ManyToManyField('Utente', related_name='iscritti')
    full = models.BooleanField(default=False)

    convalidato = models.BooleanField(default=False)

    def is_creator(self, studente):
        if studente == self.creatore:
            return True
        return False

    def __str__(self):
        return self.nome

    def contains_studente(self, studente):
        std = self.iscritti.filter(user=studente).count()
        if std < 1:
            return False
        return True

class Approvazione(models.Model):

    corso = models.ForeignKey('Corso', on_delete=models.CASCADE)
    studente = models.ForeignKey('Utente', on_delete=models.CASCADE)

    approva = models.BooleanField(default=False)

    def __str__(self):
        return self.corso.nome



class Utente(models.Model):

    nome = models.CharField(max_length=150)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    classe = models.IntegerField(default=1,validators=[MaxValueValidator(5), MinValueValidator(1)])
    sezione = models.CharField(max_length=1)

    iscrizioni = models.ManyToManyField('Corso', related_name='iscrizioni')
    hosted_courses = models.ManyToManyField('Corso')

    def is_hosted_course(self, corso):
        corsi = self.hosted_courses.filter(pk=corso.id)
        if corsi.count() == 0:
            return False
        return True

    def is_fascia_taken(self, fascia_to_check):
        iscrizione = self.iscrizioni.filter(fasce__fascia=fascia_to_check.fascia).filter(fasce__giorno=fascia_to_check.giorno).count()
        if iscrizione > 0:
            return True
        return False

    def __str__(self):
        return self.nome
