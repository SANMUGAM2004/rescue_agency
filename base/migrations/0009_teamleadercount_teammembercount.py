# Generated by Django 5.0 on 2024-01-27 03:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_remove_teamleader_user_remove_teammember_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamLeaderCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.rescueagency')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMemberCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.rescueagency')),
            ],
        ),
    ]