# Generated by Django 2.1 on 2018-10-18 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20181018_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utente',
            name='iscrizioni',
        ),
        migrations.AddField(
            model_name='utente',
            name='iscrizioni',
            field=models.ManyToManyField(related_name='iscrizioni', to='app.Corso'),
        ),
    ]
