# Generated by Django 4.0.5 on 2022-07-15 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_hospital_ambulance_available_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospital',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='hospital',
            name='longitude',
        ),
    ]