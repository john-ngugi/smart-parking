# Generated by Django 4.1.7 on 2023-03-18 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parkloader', '0004_alter_parkingloader_car_reg_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingLot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('total_slots', models.IntegerField()),
                ('available_slots', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='parkingloader',
            name='location',
        ),
        migrations.AddField(
            model_name='parkingloader',
            name='parked',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='parkingloader',
            name='parking_lot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parkloader.parkinglot'),
        ),
    ]
