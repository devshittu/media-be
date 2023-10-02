# Generated by Django 4.2.5 on 2023-10-02 02:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('message_type', models.CharField(choices=[('email', 'Email'), ('sms', 'Short Messaging Service')], default='email', max_length=5)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('subject', models.TextField(blank=True, null=True)),
                ('body', models.TextField()),
                ('variables', models.TextField(help_text='Comma separated list of expected variables')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Message Template',
                'verbose_name_plural': 'Message Templates',
            },
        ),
    ]
