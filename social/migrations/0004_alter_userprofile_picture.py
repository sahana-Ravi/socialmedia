# Generated by Django 4.0.6 on 2022-11-18 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, default='uploads/profile_pictures/default.png', upload_to='uploads/profile/pictures'),
        ),
    ]
