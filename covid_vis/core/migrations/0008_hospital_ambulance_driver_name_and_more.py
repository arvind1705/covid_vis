# Generated by Django 4.1 on 2022-09-08 05:55

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_remove_hospital_latitude_remove_hospital_longitude"),
    ]

    operations = [
        migrations.AddField(
            model_name="hospital",
            name="ambulance_driver_name",
            field=models.CharField(default="Test", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="hospital",
            name="ambulance_driver_phone",
            field=phonenumber_field.modelfields.PhoneNumberField(
                default="+91-232326401", max_length=128, region=None
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="hospital",
            name="image_link",
            field=models.CharField(
                default="https://thumbs.dreamstime.com/z/hospital-building-modern-parking-lot-59693686.jpg",
                max_length=500,
            ),
            preserve_default=False,
        ),
    ]
