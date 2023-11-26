# Generated by Django 4.2.1 on 2023-11-22 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_adminprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrepreneurprofile',
            name='linkedin_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='role',
            field=models.CharField(choices=[('investor', 'Investor'), ('entrepreneur', 'Entrepreneur'), ('admin', 'Admin')], default='entrepreneur', max_length=15),
        ),
        migrations.AlterField(
            model_name='entrepreneurprofile',
            name='profile_picture',
            field=models.FileField(blank=True, null=True, upload_to='entrepreneur_profile/'),
        ),
        migrations.AlterField(
            model_name='investorprofile',
            name='profile_picture',
            field=models.FileField(blank=True, null=True, upload_to='investor_profile/'),
        ),
    ]
