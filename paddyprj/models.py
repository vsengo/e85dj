from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Project
from datetime import datetime

# Tables to manage investment and expenses
TXTYPE =[
    ('DEPOSIT','Deposit'),
    ('WITHDRAWAL','Withdraw'),
    ('INCOME','Interest'),
]

class ExpenseType(models.Model):
    expense = models.CharField(max_length=16)
    
    def __str__(self):
        return "%s " % (self.expense)

class PaddyProject(models.Model):
    project = models.OneToOneField(Project,on_delete=models.CASCADE)
    costPerShare = models.DecimalField(max_digits=9,decimal_places=2,default=0)
    totalShares = models.IntegerField(default=0)
    landArea = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    costPrep = models.IntegerField(default=0)
    costSeed = models.IntegerField(default=0)
    costFertilizer = models.IntegerField(null=True)
    costHarvest = models.IntegerField(default=0)
    costStorage = models.IntegerField(null=True)
    estHarvest = models.IntegerField(null=True)    #In kg
    estSalePrice = models.IntegerField(null=True)  #Per kg
    contract = models.CharField(max_length=2000,null=True)

@receiver(post_save, sender=Project)
def create_project_paddyproject(sender, instance, created, **kwargs):
    if created:
        PaddyProject.objects.create(project=instance)

@receiver(post_save, sender=Project)
def save_project_paddyproject(sender, instance, **kwargs):
    instance.paddyproject.save()

class Investor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(PaddyProject, on_delete=models.CASCADE)
    amount = models.IntegerField(max_length=9)
    startDate = models.DateField(default=datetime.now())
    endDate = models.DateField(null=True)
    updatedOn = models.DateTimeField(default=datetime.now())

class Transaction(models.Model):
    project = models.ForeignKey(PaddyProject, on_delete=models.CASCADE)
    txOwner = models.ForeignKey(User, related_name='txOwner', on_delete=models.CASCADE)
    txType = models.CharField(max_length=10,choices=TXTYPE)
    exType = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    remarks=models.CharField(max_length=100,blank=True,null=True)
    amount = models.IntegerField(max_length=9)
    date = models.DateField(default=datetime.now())
    updatedBy = models.ForeignKey(User,on_delete=models.CASCADE)
    updatedOn = models.DateTimeField(default=datetime.now())

#Tables to provide status updates
class ProjectUpdate(models.Model):
    project = models.ForeignKey(PaddyProject, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=2000)
    reviewedBy = models.ForeignKey(User, related_name='reviewer', on_delete=models.CASCADE, null=True)
    updatedBy = models.ForeignKey(User, related_name='contributor', on_delete=models.CASCADE)
    updatedOn = models.DateTimeField(default=datetime.now())

class Photo(models.Model):
    file = models.ImageField(upload_to='photos/%Y', blank=True,null=True)
    figNo = models.IntegerField(default=0)
    thumb = models.ImageField(upload_to='photos/%Y', blank=True,null=True)
    project = models.ForeignKey(ProjectUpdate, related_name='album', on_delete=models.CASCADE)
    updatedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    updatedOn = models.DateTimeField(default=datetime.now())

class Video(models.Model):
    file = models.FileField(upload_to='videow/%Y',blank=True, null=True)
    project = models.ForeignKey(ProjectUpdate, related_name='video', on_delete=models.CASCADE)
    updatedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    updatedOn = models.DateTimeField(default=datetime.now())
