# Generated by Django 4.2.5 on 2023-09-25 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stories', '0001_initial'),
        ('analytics', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='usersession',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_sessions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usernotinterested',
            name='story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.story'),
        ),
        migrations.AddField(
            model_name='usernotinterested',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uninterested_stories', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='storyinteractionmetadataschema',
            unique_together={('interaction_type', 'version')},
        ),
        migrations.AddField(
            model_name='storyinteraction',
            name='story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interactions', to='stories.story'),
        ),
        migrations.AddField(
            model_name='storyinteraction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='story_interactions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='storyinteraction',
            name='user_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interactions', to='analytics.usersession'),
        ),
        migrations.AddField(
            model_name='accessibilitytool',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accessibility_tools', to=settings.AUTH_USER_MODEL),
        ),
    ]
