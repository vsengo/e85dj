from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
# Create your models here.

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.TextField(max_length=12, blank=True)
    city = models.CharField(max_length=30, blank=True)
    dob = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=30, blank=True)
    def __str__(self):
        return "%s " % (self.user.first_name) 

@receiver(post_save, sender=User)
def create_user_member(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_member(sender, instance, **kwargs):
    instance.member.save()

class Project(models.Model):
    NOT_STARTED = 'NS'
    IN_PROGRESS = 'PR'
    COMPLETED   = 'CP'
    CANCELLED   = 'CX'
    PROJ_STATUS = [
            (NOT_STARTED,'Not Started'),
            (IN_PROGRESS,'In Progress'),
            (COMPLETED,'Completed'),
            (CANCELLED,'Cancelled'),
    ]
    
    PROJ_TYPE_PADDY='INVESTMENT'
    PROJ_TYPE_CHARITY='CHARITY'

    PROJ_TYPE=[
        (PROJ_TYPE_CHARITY,'Charitable'),
        (PROJ_TYPE_PADDY,'Investment'),
    ]

    name = models.CharField(max_length=64)
    purpose = models.TextField(max_length=2000, blank=True)
    status = models.CharField(max_length=3,choices=PROJ_STATUS,default=NOT_STARTED)
    startDate = models.DateField(default=datetime.now())
    endDate = models.DateField(null=True, blank=True)
    currentFund = models.IntegerField(null=True)
    futureFund = models.IntegerField(null=True)
    targetFund = models.IntegerField(null=True)
    updatedBy = models.ForeignKey(User,on_delete=models.CASCADE)
    updatedOn = models.DateTimeField(default=datetime.now())
    prjType = models.CharField(max_length=12,choices=PROJ_TYPE,default=PROJ_TYPE_CHARITY)

class Role(models.Model):
    title = models.CharField(max_length=64, blank=False, help_text="name")
    
    def __str__(self):
        return "%s " % (self.title) 

class Commitee(models.Model):
    CURRENT = 'CR'
    PAST    = 'PS'
    COMMITEE_STATUS = [
            (CURRENT,'Current'),
            (PAST,'Past'),
    ]
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    member=models.ForeignKey(Member, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=2,choices=COMMITEE_STATUS,default=CURRENT)
    startDate = models.DateField(default=datetime.now())
    endDate = models.DateField(null=True, blank=True)
    updatedBy = models.ForeignKey(User,on_delete=models.CASCADE)
    updatedOn = models.DateTimeField(default=datetime.now())

class Minute(models.Model):
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    attendees=models.CharField(max_length=500)
    discussion = models.CharField(max_length=2000)
    resolution = models.CharField(max_length=1000)
    todos      = models.CharField(max_length=1000)
    date = models.DateField(null=True, blank=True)
    updatedBy = models.ForeignKey(User,on_delete=models.CASCADE)
    updatedOn = models.DateTimeField(default=datetime.now())