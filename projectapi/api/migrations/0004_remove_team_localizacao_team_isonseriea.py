# Generated by Django 4.2.7 on 2023-11-24 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_team'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='localizacao',
        ),
        migrations.AddField(
            model_name='team',
            name='isOnSerieA',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]