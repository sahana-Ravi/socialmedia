# Generated by Django 4.0.6 on 2022-11-18 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0012_alter_userprofile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, default='uploads/profile_pictures/profile.jpg', null=True, upload_to='uploads/profile_pictures'),
        ),
    ]
