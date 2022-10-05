from urllib.request import DataHandler
from xml.etree.ElementTree import Comment
from django import forms
from django.contrib.auth.models import User
from accounts.forms import ProjectForm
from util.widgets import BootstrapDateTimePickerInput
from .models import Investor, PaddyProject, Investor
from .models import ProjectStatus, Comment

class PaddyPrjForm(forms.ModelForm):
    class Meta:
        model = PaddyProject
        fields = ['contract','costPerShare','totalShares','landArea','costPrep','costSeed','costFertilizer','costHarvest','costStorage','estHarvest','estSalePrice']

    def save(self, commit=True):
        data = super(PaddyPrjForm, self).save(commit=False)
        if commit:
            data.save()

        return DataHandler

class InvestorForm(forms.ModelForm):
    class Meta:
        model = Investor
        fields = ['user','shares','startDate','endDate']
    
    def save(self, commit=True):
        data = super(InvestorForm, self).save(commit=False)
        if commit:
            data.save()

        return data

class ProjectStatusForm(forms.ModelForm):
    class Meta:
        model = ProjectStatus
        fields = ['title','content','photo','video']

    def save(self, commit=True):
        data = super(ProjectStatusForm, self).save(commit=False)
        if commit:
            data.save()

        return data

    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body','link']

    def save(self, commit=True):
        data = super(CommentForm, self).save(commit=False)
        if commit:
            data.save()

        return data
