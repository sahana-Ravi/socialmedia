# Generated by Django 4.0.6 on 2022-11-18 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_alter_userprofile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, default='uploads/profile/pictures/default_3JACeb7.png', upload_to='uploads/profile/pictures'),
        ),
    ]
