# Generated by Django 4.1.7 on 2023-03-19 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parkloader', '0006_billingplan_parkingloader_user_billing_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parkingloader',
            old_name='billing',
            new_name='plan',
        ),
        migrations.RemoveField(
            model_name='billing',
            name='plan',
        ),
        migrations.AddField(
            model_name='billing',
            name='Billingplan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parkloader.billingplan'),
        ),
    ]