# Generated by Django 4.1.1 on 2022-09-25 00:09

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_commitee_startdate_alter_commitee_updatedon_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('batchfund', '0006_rename_period_contribution_frequency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='currency',
            field=models.CharField(choices=[('Rs', 'Rs'), ('CA$', 'C$'), ('US$', 'US$'), ('SG$', 'SG$'), ('GBP', 'GBP'), ('AU$', 'AU$')], default='Rs', max_length=3),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='frequency',
            field=models.CharField(choices=[('Month', 'Monthly'), ('Year', 'Yearly'), ('Once', 'Once')], default='Month', max_length=5),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.project'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2022, 9, 25, 0, 9, 19, 941997)),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='updatedOn',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 25, 0, 9, 19, 942011)),
        ),
        migrations.AlterField(
            model_name='contributionhist',
            name='status',
            field=models.CharField(choices=[('Committed', 'Committed'), ('Transferred', 'Transfered')], default='Committed', max_length=12),
        ),
        migrations.AlterField(
            model_name='contributionhist',
            name='updatedOn',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 25, 0, 9, 19, 942348)),
        ),
        migrations.CreateModel(
            name='DistributionHist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(max_length=16)),
                ('status', models.CharField(choices=[('Committed', 'Committed'), ('Transferred', 'Transfered')], default='transferred', max_length=12)),
                ('updatedOn', models.DateTimeField(default=datetime.datetime(2022, 9, 25, 0, 9, 19, 943466))),
                ('contribution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='batchfund.contribution')),
                ('updatedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Distribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested', models.IntegerField(max_length=9)),
                ('committed', models.IntegerField(max_length=9)),
                ('currency', models.CharField(choices=[('Rs', 'Rs'), ('CA$', 'C$'), ('US$', 'US$'), ('SG$', 'SG$'), ('GBP', 'GBP'), ('AU$', 'AU$')], default='Rs', max_length=3)),
                ('distrDate', models.DateField(default=datetime.datetime(2022, 9, 25, 0, 9, 19, 942577))),
                ('frequency', models.CharField(choices=[('Month', 'Monthly'), ('Year', 'Yearly'), ('Once', 'Once')], default='Once', max_length=5)),
                ('status', models.CharField(choices=[('Committed', 'Committed'), ('Transferred', 'Transfered')], default='Committed', max_length=12)),
                ('updatedOn', models.DateTimeField(default=datetime.datetime(2022, 9, 25, 0, 9, 19, 942604))),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.project')),
                ('updatedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
