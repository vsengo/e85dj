# Generated by Django 4.1.1 on 2022-09-23 20:27

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_commitee_status_commitee_updatedby_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commitee',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2022, 9, 23, 20, 27, 13, 789572)),
        ),
        migrations.RemoveField(
            model_name='commitee',
            name='updatedBy',
        ),
        migrations.AlterField(
            model_name='commitee',
            name='updatedOn',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 23, 20, 27, 13, 789592)),
        ),
        migrations.AlterField(
            model_name='project',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2022, 9, 23, 20, 27, 13, 788969)),
        ),
        migrations.RemoveField(
            model_name='project',
            name='updatedBy',
        ),
        migrations.AlterField(
            model_name='project',
            name='updatedOn',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 23, 20, 27, 13, 789011)),
        ),
        migrations.AddField(
            model_name='commitee',
            name='updatedBy',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='updatedBy',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
