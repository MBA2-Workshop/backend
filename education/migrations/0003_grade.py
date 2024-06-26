# Generated by Django 5.0.6 on 2024-06-20 10:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_alter_training_instructor_alter_training_students'),
        ('event', '0003_event_training'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('coefficient', models.IntegerField(blank=True, default=1)),
                ('value', models.FloatField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade_event', to='event.event')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade_training', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grade_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
