# Generated by Django 4.1.7 on 2023-03-17 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkloader', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingloader',
            name='location',
            field=models.TextField(max_length=70),
        ),
    ]
