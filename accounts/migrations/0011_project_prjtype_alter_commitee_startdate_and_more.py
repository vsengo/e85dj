# Generated by Django 4.1.1 on 2022-09-26 21:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_commitee_startdate_alter_commitee_updatedon_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='prjType',
            field=models.CharField(choices=[('CHARITY', 'Charitable'), ('INVESTMENT', 'Investment')], default='CHARITY', max_length=12),
        ),
        migrations.AlterField(
            model_name='commitee',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2022, 9, 26, 21, 29, 4, 204175)),
        ),
        migrations.AlterField(
            model_name='commitee',
            name='updatedOn',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 26, 21, 29, 4, 204195)),
        ),
        migrations.AlterField(
            model_name='minute',
            name='updatedOn',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 26, 21, 29, 4, 204465)),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='project',
            name='purpose',
            field=models.TextField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='project',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2022, 9, 26, 21, 29, 4, 203674)),
        ),
        migrations.AlterField(
            model_name='project',
            name='updatedOn',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 26, 21, 29, 4, 203718)),
        ),
    ]
