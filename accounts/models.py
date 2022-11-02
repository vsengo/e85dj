from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils  import timezone

class UserRole:
    EDIT='EDIT'
    VIEW='VIEW'
    NONE='NONE'
    
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.TextField(max_length=12, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)    
    photo = models.ImageField(upload_to='profile/',blank=True, null=True)

    def __str__(self):
        return "%s %" % (self.first_name,self.last_name) 

@receiver(post_save, sender=User)
def create_user_member(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_member(sender, instance, **kwargs):
    instance.member.save()

class ProjectType(models.Model):
    description=models.CharField(max_length=32,null=True)

    def __str__(self):
        return "%s " % (self.description) 

class Project(models.Model):
    NOT_STARTED = 'NotStarted'
    IN_PROGRESS = 'InProgress'
    COMPLETED   = 'Completed'
    CANCELLED   = 'Cancelled'
    PROJ_STATUS = [
            (NOT_STARTED,'Not Started'),
            (IN_PROGRESS,'In Progress'),
            (COMPLETED,'Completed'),
            (CANCELLED,'Cancelled'),
    ]
    
    name = models.CharField(max_length=64)
    purpose = models.TextField(max_length=2000, blank=True)
    status = models.CharField(max_length=10,choices=PROJ_STATUS,default=NOT_STARTED)
    startDate = models.DateField(default=timezone.now)
    endDate = models.DateField(null=True, blank=True)
    raisedFund = models.IntegerField(null=True)
    spentFund = models.IntegerField(null=True)
    targetFund = models.IntegerField(null=True)
    participants = models.IntegerField(null=True,default=0)
    updatedBy = models.ForeignKey(User,on_delete=models.PROTECT)
    updatedOn = models.DateTimeField(default=timezone.now)
    prjType = models.ForeignKey(ProjectType, on_delete=models.PROTECT)

    def isCommiteeMember(self, user):
        member= Member.objects.get(user_id=user.id)
        committee = Commitee.objects.all().filter(project_id=self.id).filter(member_id = member.id)
        if committee.exists():
            return True
        return False
    
    def getUserRole(self, user, table):
        member= User.objects.get(id=user.id)
        committee = Commitee.objects.all().filter(project_id=self.id).filter(member_id = member.id).first()
        if committee == None:
            return UserRole.VIEW
        
        role = RoleEdit.objects.all().filter(role_id=committee.role_id).filter(canEdit=table)
        if role.exists():
            return UserRole.EDIT

        return UserRole.VIEW

    def __str__(self):
        return "%s " % (self.name) 

class Role(models.Model):
    title = models.CharField(max_length=64, blank=False, help_text="name")
    priority = models.SmallIntegerField()
    
    def __str__(self):
        return "%s " % (self.title) 

class RoleEdit(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    canEdit = models.CharField (max_length=24)

class Commitee(models.Model):
    CURRENT = 'Current'
    PAST    = 'Past'
    COMMITEE_STATUS = [
            (CURRENT,'Current'),
            (PAST,'Past'),
    ]
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    member=models.ForeignKey(User, related_name='commitee_member', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=7,choices=COMMITEE_STATUS,default=CURRENT)
    startDate = models.DateField(default=timezone.now)
    endDate = models.DateField(null=True, blank=True)
    updatedBy = models.ForeignKey(User,on_delete=models.PROTECT)
    updatedOn = models.DateTimeField(default=timezone.now)

class Minute(models.Model):
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    attendees=models.TextField(max_length=500)
    discussion = models.TextField(max_length=2000)
    resolution = models.TextField(max_length=1000)
    todos      = models.TextField(max_length=1000)
    date = models.DateField(default=timezone.now)
    updatedBy = models.ForeignKey(User,on_delete=models.PROTECT)
    updatedOn = models.DateTimeField(default=timezone.now)

class ExpenseType(models.Model):
    expense = models.CharField(max_length=16)
    prjType = models.ForeignKey(ProjectType, on_delete=models.CASCADE)
    
    def __str__(self):
        return "%s " % (self.expense)

class BankAccount(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    holder = models.ForeignKey(User,related_name='holder', on_delete=models.PROTECT)
    name = models.CharField(max_length=32)
    purpose = models.CharField(max_length=128,null=True,blank=True)
    bank = models.CharField(max_length=32)
    accNumber = models.CharField(max_length=32)
    branch = models.CharField(max_length=128)
    routing = models.CharField(max_length=128)
    telno = models.CharField(max_length=12, null=True, blank=True)
    email = models.CharField(max_length=32,null=True, blank=True)
    balance = models.DecimalField(max_digits=12,decimal_places=2,default=0.0)  
    updatedBy = models.ForeignKey(User,on_delete=models.CASCADE)
    updatedOn = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "%s - %s" % (self.project.name,self.name)

class Transaction(models.Model):
    TxType_DEPOSIT='DEPOSIT'
    TxType_WITHDRWAL='WITHDRAWAL'
    TxType_INCOME='INTEREST'
    TxType_FEES = 'FEES'

    TXTYPE =[
        (TxType_DEPOSIT,'Deposit'),
        (TxType_WITHDRWAL,'Withdraw'),
        (TxType_INCOME,'Interest'),
        (TxType_FEES,'fees'),
    ]
    TXCONFIRM = [
        ('Unconfirmed',"Unconfirmed"),
        ('Confirmed',"Confirmed"),
    ]

    bank = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='Owner', on_delete=models.PROTECT)
    txType  = models.CharField(max_length=10,choices=TXTYPE)
    exType  = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    remarks =models.TextField(max_length=100,blank=True,null=True)
    amount  = models.IntegerField()
    date    = models.DateField(default=timezone.now)
    receipt = models.FileField(upload_to='transaction/%Y',null=True,blank=True)
    confirmed = models.CharField(max_length=16,choices=TXCONFIRM,default='UnConfirmed')
    updatedBy = models.ForeignKey(User,on_delete=models.PROTECT)
    updatedOn = models.DateTimeField(default=timezone.now)


