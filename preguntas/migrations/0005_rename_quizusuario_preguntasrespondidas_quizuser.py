# Generated by Django 3.2.6 on 2021-08-24 22:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preguntas', '0004_rename_usuario_preguntasrespondidas_quizusuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='preguntasrespondidas',
            old_name='quizusuario',
            new_name='quizUser',
        ),
    ]
