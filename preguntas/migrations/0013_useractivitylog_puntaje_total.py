# Generated by Django 3.2.6 on 2021-08-29 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preguntas', '0012_alter_useractivitylog_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='useractivitylog',
            name='puntaje_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Puntaje Total'),
        ),
    ]