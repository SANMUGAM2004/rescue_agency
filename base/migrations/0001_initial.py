# Generated by Django 5.0 on 2024-01-23 18:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RescueAgency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization_name', models.CharField(max_length=255)),
                ('organization_type', models.CharField(choices=[('tsunami', 'Tsunami'), ('flood', 'Flood'), ('cyclone', 'Cyclone'), ('earthquake', 'Earthquake'), ('storm', 'Storm')], max_length=20)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=20)),
                ('admin_name', models.CharField(max_length=255)),
                ('team_member_count', models.IntegerField()),
                ('organization_location', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('profile', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.profile')),
            ],
        ),
    ]
