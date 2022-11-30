from django.db import models
from django.contrib.auth.models import User 
from django.utils  import timezone
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
    amount = models.IntegerField()
    currency = models.CharField(max_length=3,choices=CURRENCY, default='Rs')
    frequency = models.CharField(max_length=5,choices=FREQUENCY,default='Month')
    startDate = models.DateField(default=timezone.now)
    endDate = models.DateField(null=True, blank=True)
    updatedBy = models.ForeignKey(User,related_name='Contrb_updatedBy',on_delete=models.CASCADE)
    updatedOn = models.DateTimeField(default=timezone.now)

class Distribution(models.Model):
    def __str__(self):
        return self.get_frequency_display()
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    purpose = models.TextField(max_length=500)
    requested = models.IntegerField()
    committed = models.IntegerField(null=True)
    currency = models.CharField(max_length=3,choices=CURRENCY, default='Rs')
    distrDate = models.DateField(default=timezone.now)
    frequency = models.CharField(max_length=5,choices=FREQUENCY,default='Once')
    status = models.CharField(max_length=12,choices=STATUS,default='Committed')
    updatedBy = models.ForeignKey(User,on_delete=models.CASCADE)
    updatedOn = models.DateTimeField(default=timezone.now)

class IncomeReport(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    period=models.CharField(max_length=16,null=False) 
    amount=models.IntegerField(null=True,default=0)
    count=models.IntegerField(null=True,default=0)   
