# Generated by Django 5.1.7 on 2025-04-11 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_post_bio_post_profile_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='profile_picture',
            new_name='media',
        ),
    ]
