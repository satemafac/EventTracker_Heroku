# Generated by Django 4.0.4 on 2022-07-23 14:31

from django.db import migrations, models
import event.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_auto_20220524_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_code',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_code_short',
            field=models.CharField(default=event.models.Event.short_unique, max_length=10),
        ),
        migrations.AlterField(
            model_name='event_attendee',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='event_host',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
