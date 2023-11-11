# Generated by Django 3.2.12 on 2022-11-10 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0001_initial'),
        ('events', '0019_event_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrant',
            name='certification_track',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, to='trainings.certification'),
        ),
    ]
