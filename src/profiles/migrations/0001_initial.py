# Generated by Django 5.1.1 on 2024-09-11 12:44

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
                ('role', models.CharField(choices=[('organizer', 'Organizer'), ('attendee', 'Attendee')], max_length=20)),
                ('profilePicture', models.ImageField(default='userPlaceHolder.png', upload_to='ProfilePictures')),
                ('firstName', models.CharField(blank=True, max_length=35)),
                ('lastName', models.CharField(blank=True, max_length=35)),
                ('email', models.EmailField(blank=True, max_length=90)),
                ('updated', models.TimeField(auto_now=True)),
                ('created', models.TimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
