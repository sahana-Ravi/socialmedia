# Generated by Django 4.0.6 on 2022-11-19 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0017_post_dislikes_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.FileField(blank=True, default='uploads/profile_pictures/default.png', upload_to='uploads/profile/pictures'),
        ),
    ]
