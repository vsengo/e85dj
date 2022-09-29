# Generated by Django 4.1.1 on 2022-09-26 21:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('batchfund', '0009_alter_contribution_startdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2022, 9, 26, 21, 29, 4, 204979)),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='updatedOn',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 26, 21, 29, 4, 204989)),
        ),
        migrations.AlterField(
            model_name='contributionhist',
            name='updatedOn',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 26, 21, 29, 4, 205246)),
        ),
        migrations.AlterField(
            model_name='distribution',
            name='distrDate',
            field=models.DateField(default=datetime.datetime(2022, 9, 26, 21, 29, 4, 205992)),
        ),
        migrations.AlterField(
            model_name='distribution',
            name='updatedOn',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 26, 21, 29, 4, 206018)),
        ),
        migrations.AlterField(
            model_name='distributionhist',
            name='updatedOn',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 26, 21, 29, 4, 206256)),
        ),
    ]
