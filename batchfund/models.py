from django.db import models
from django.contrib.auth.models import User 
from datetime import datetime
from accounts.models import Project
    
STATUS = [
    ('Committed','Committed'),
    ('Transferred','Transfered'),
]

CURRENCY = [
    ('Rs','Rs'),
    ('CA$','C$'),
    ('US$','US$'),
    ('SG$','SG$'),
    ('GBP','GBP'),
    ('AU$','AU$'),
]
FREQUENCY = [
    ('Month','Monthly'),
    ('Year','Yearly'),
    ('Once','Once'),
]
class Contribution(models.Model):
    def __str__(self):
        return self.get_frequency_display()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.IntegerField(max_length=9)
    currency = models.CharField(max_length=3,choices=CURRENCY, default='Rs')
    frequency = models.CharField(max_length=5,choices=FREQUENCY,default='Month')
    startDate = models.DateField(default=datetime.now())
    endDate = models.DateField(null=True, blank=True)
    updatedOn = models.DateTimeField(default=datetime.now())

class ContributionHist(models.Model):  

    contribution=models.ForeignKey(Contribution,on_delete=models.CASCADE)
    amount = models.IntegerField(max_length=16)
    status = models.CharField(max_length=12,choices=STATUS,default='Committed')
    updatedBy = models.ForeignKey(User,on_delete=models.CASCADE)
    updatedOn = models.DateTimeField(default=datetime.now())

class Distribution(models.Model):
    def __str__(self):
        return self.get_frequency_display()
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    requested = models.IntegerField(max_length=9)
    committed = models.IntegerField(max_length=9)
    currency = models.CharField(max_length=3,choices=CURRENCY, default='Rs')
    distrDate = models.DateField(default=datetime.now())
    frequency = models.CharField(max_length=5,choices=FREQUENCY,default='Once')
    status = models.CharField(max_length=12,choices=STATUS,default='Committed')
    updatedBy = models.ForeignKey(User,on_delete=models.CASCADE)
    updatedOn = models.DateTimeField(default=datetime.now())

class DistributionHist(models.Model):  
    contribution=models.ForeignKey(Contribution,on_delete=models.CASCADE)
    amount = models.IntegerField(max_length=16)
    status = models.CharField(max_length=12,choices=STATUS,default='transferred')
    updatedBy = models.ForeignKey(User,on_delete=models.CASCADE)
    updatedOn = models.DateTimeField(default=datetime.now())