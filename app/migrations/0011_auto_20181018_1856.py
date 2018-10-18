# Generated by Django 2.1 on 2018-10-18 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20181018_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_aula', models.CharField(max_length=100)),
                ('capacita', models.IntegerField(default=30)),
            ],
        ),
        migrations.AddField(
            model_name='corso',
            name='corso_id',
            field=models.IntegerField(default='1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='corso',
            name='aula',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='aula', to='app.Aula'),
            preserve_default=False,
        ),
    ]
