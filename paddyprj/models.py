from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Project
from django.utils  import timezone

# Tables to manage investment and expenses
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
    shares = models.IntegerField()
    startDate = models.DateField(default=timezone.now)
    endDate = models.DateField(null=True, blank=True)
    updatedOn = models.DateTimeField(default=timezone.now)

#Tables to provide status updates
class ProjectStatus(models.Model):
    project = models.ForeignKey(PaddyProject, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    content = models.TextField(max_length=2000)
    photo = models.ImageField(upload_to='paddyprj/%Y',blank=True, null=True)
    video = models.FileField(upload_to='paddyprj/%Y',blank=True, null=True)
    link = models.URLField(blank=True, null=True, help_text="Optional: any link to share")
    likes = models.PositiveSmallIntegerField(default=0)
    dislikes = models.PositiveSmallIntegerField(default=0)
    comments = models.PositiveSmallIntegerField(default=0)
    reviewedBy = models.ForeignKey(User, related_name='reviewer', on_delete=models.CASCADE, null=True)
    updatedBy = models.ForeignKey(User, related_name='updatedBy', on_delete=models.CASCADE)
    updatedOn = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    status = models.ForeignKey(ProjectStatus, on_delete=models.CASCADE)
    body = models.TextField(max_length=256)
    link = models.URLField(blank=True, null=True, help_text="Optional: any link to share")
    updatedBy = models.ForeignKey(User, related_name='commentor', on_delete=models.CASCADE)
    updatedOn = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['-updatedOn']

    def __str__(self):
        return 'Comment {} by {} on {}'.format(self.body, self.updatedBy.first_name, self.updatedOn)
