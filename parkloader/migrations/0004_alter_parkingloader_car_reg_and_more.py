# Generated by Django 4.1.7 on 2023-03-18 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkloader', '0003_alter_parkingloader_vehicle_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingloader',
            name='car_reg',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='parkingloader',
            name='location',
            field=models.CharField(max_length=70),
        ),
    ]
