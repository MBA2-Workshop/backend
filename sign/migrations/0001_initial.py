# Generated by Django 5.0.6 on 2024-06-20 11:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('education', '0002_alter_training_instructor_alter_training_students'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('signed', models.BooleanField(default=False)),
                ('instructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sign_instructor', to=settings.AUTH_USER_MODEL)),
                ('training', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='education.training')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
