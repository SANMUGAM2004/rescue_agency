# Generated by Django 5.0 on 2024-01-24 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('main_admin', 'Main Admin'), ('rescue_agency_admin', 'Rescue Agency Admin'), ('rescue_agency_team_leader', 'Rescue Agency Team Leader'), ('rescue_agency_team_member', 'Rescue Agency Team Member')], default='rescue_agency_admin', max_length=30),
        ),
    ]
