# Generated by Django 5.0.6 on 2024-06-19 12:30

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('cfa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_cfa', to=settings.AUTH_USER_MODEL)),
                ('instructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='training_instructor', to=settings.AUTH_USER_MODEL)),
                ('students', models.ManyToManyField(related_name='training_students', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
