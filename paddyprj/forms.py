from urllib.request import DataHandler
from django import forms
from django.contrib.auth.models import User
from accounts.forms import ProjectForm
from util.widgets import BootstrapDateTimePickerInput
from .models import ExpenseType, Investor, PaddyProject, Transaction, Investor

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
        fields = ['amount','startDate','endDate']
    
    def save(self, commit=True):
        data = super(InvestorForm, self).save(commit=False)
        if commit:
            data.save()

        return DataHandler

class TransactionForm(forms.ModelForm):
    exType=forms.ModelChoiceField(queryset=ExpenseType.objects.filter())
    class Meta:
        model = Transaction
        fields = ['txOwner','txType','exType','remarks','amount','date']

    def save(self, commit=True):
        data = super(TransactionForm, self).save(commit=False)
        if commit:
            data.save()

        return data