# Generated by Django 4.0.5 on 2022-07-12 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_patient_covid_positive'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='is_covid_care_center',
            field=models.BooleanField(default=False),
        ),
    ]