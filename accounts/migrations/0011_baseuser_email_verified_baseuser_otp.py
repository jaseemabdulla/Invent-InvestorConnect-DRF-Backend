# Generated by Django 4.2.7 on 2023-12-24 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_entrepreneurprofile_mentor'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='email_verified',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
