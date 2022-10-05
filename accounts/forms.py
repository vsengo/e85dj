from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from util.widgets import BootstrapDateTimePickerInput
from .models import Commitee, Member, Project, Role, Minute, ExpenseType, Transaction

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "First Name")
    last_name = forms.CharField(label = "Last Name")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserForm(forms.ModelForm):
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label = "First Name")
    last_name = forms.CharField(label = "Last Name")

    class Meta:
        model=User
        fields = ("first_name","last_name","email")

class MemberForm(forms.ModelForm):
    mobile =forms.CharField(label="Mobile Number (country) (number)")
    city = forms.CharField(label = "City")
    country = forms.CharField(label = "Country")
    dob = forms.DateField(label = "Date of Birth",)
    widgets = {
            'dob': BootstrapDateTimePickerInput(format='%Y-%m-%d'), # specify date-frmat
        }
    class Meta:
        model = Member
        fields = ("mobile","city", "country", "dob",'photo')
    
    def save(self,commit=True):
        member = super(MemberForm,self).save(commit=False)
        if commit:
            member.save()
        return member

class ProjectForm(forms.ModelForm):
    widgets = {
            'startDate': BootstrapDateTimePickerInput(format='%Y-%m-%d'), # specify date-frmat
            'ebdDate'  : BootstrapDateTimePickerInput(format='%Y-%m-%d'), # specify date-frmat
        }
    class Meta:
        model = Project
        fields = ('name','purpose','prjType','status','startDate','endDate','targetFund')
    
    def save(self,commit=True):
        project = super(ProjectForm,self).save(commit=False)
        if commit:
            project.save()
        return project

class CommiteeForm(forms.ModelForm):
    widgets = {
            'startDate': BootstrapDateTimePickerInput(format='%Y-%m-%d'), # specify date-frmat
            'endDate'  : BootstrapDateTimePickerInput(format='%Y-%m-%d'), # specify date-frmat
        }

    role=forms.ModelChoiceField(queryset=Role.objects.filter())
    member=forms.ModelChoiceField(queryset=Member.objects.filter())

    class Meta:
        model = Commitee
        fields = ('member','role','status','startDate','endDate')
    
    def save(self,commit=True):
        data = super(CommiteeForm,self).save(commit=False)
        if commit:
            data.save()
        return data

class MinuteForm(forms.ModelForm):
    widgets = {
            'date': BootstrapDateTimePickerInput(format='%Y-%m-%d'), # specify date-frmat
        }
    class Meta:
        model = Minute
        fields = ('attendees','discussion','resolution','todos','date')
    
    def save(self,commit=True):
        data = super(MinuteForm,self).save(commit=False)
        if commit:
            data.save()
        return data

class TransactionForm(forms.ModelForm):
    exType=forms.ModelChoiceField(queryset=ExpenseType.objects.filter())
    class Meta:
        model = Transaction
        fields = ['txOwner','txType','exType','remarks','amount','receipt','date']

    def save(self, commit=True):
        data = super(TransactionForm, self).save(commit=False)
        if commit:
            data.save()

        return data