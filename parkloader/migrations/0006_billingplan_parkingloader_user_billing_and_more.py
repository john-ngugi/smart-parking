# Generated by Django 4.1.7 on 2023-03-19 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parkloader', '0005_parkinglot_remove_parkingloader_location_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('max_bookings', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='parkingloader',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(max_length=50)),
                ('card_number', models.CharField(max_length=20)),
                ('card_expiry', models.CharField(max_length=10)),
                ('cvv', models.CharField(max_length=5)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='parkingloader',
            name='billing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parkloader.billing'),
        ),
    ]
