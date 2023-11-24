# Generated by Django 4.2.7 on 2023-11-24 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_profile_options_alter_profile_managers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('data_fundacao', models.DateField()),
                ('cores', models.CharField(max_length=200)),
                ('localizacao', models.CharField(max_length=100)),
            ],
        ),
    ]