# Generated by Django 2.2.28 on 2024-08-13 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_event_users_is_event_guest_event_users_is_event_host_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_attendee',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='event_host',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
