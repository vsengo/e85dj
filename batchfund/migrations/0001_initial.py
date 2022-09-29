# Generated by Django 4.1.1 on 2022-09-23 20:09

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_commitee_status_commitee_updatedby_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(max_length=16)),
                ('status', models.CharField(choices=[('CMTD', 'Committed'), ('TRFD', 'Transfered')], default='CMTD', max_length=4)),
                ('period', models.CharField(choices=[('MONTH', 'Monthly'), ('YEAR', 'Yearly'), ('ADHOC', 'Adhoc')], default='MONTH', max_length=5)),
                ('startDate', models.DateField(default=datetime.datetime(2022, 9, 23, 20, 8, 48, 714649))),
                ('endDate', models.DateField(blank=True, null=True)),
                ('updatedOn', models.DateTimeField(default=datetime.datetime(2022, 9, 23, 20, 8, 48, 714659))),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.project')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContributionHist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(max_length=16)),
                ('updatedOn', models.DateTimeField(default=datetime.datetime(2022, 9, 23, 20, 8, 48, 714911))),
                ('contribution', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='batchfund.contribution')),
                ('updatedBy', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
