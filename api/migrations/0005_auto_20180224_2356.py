# Generated by Django 2.0.2 on 2018-02-24 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_seat_time_slot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='time_slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.TimeSlot'),
        ),
    ]