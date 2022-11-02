from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from util.widgets import BootstrapDateTimePickerInput
from .models import Commitee, Member, Project, Role, Minute, ExpenseType, Transaction, BankAccount

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
    mobile =forms.CharField(label="Mobile Number (countrycode number)")
    city = forms.CharField(label = "City")
    country = forms.CharField(label = "Country")
    dob = forms.DateField(label = "Date of Birth(YYYY-MM-DD)",)
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

class MemberChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "%s %s" % (obj.first_name, obj.last_name)

class CommiteeForm(forms.ModelForm):
    widgets = {
            'startDate': BootstrapDateTimePickerInput(format='%Y-%m-%d'), # specify date-frmat
            'endDate'  : BootstrapDateTimePickerInput(format='%Y-%m-%d'), # specify date-frmat
        }

    role=forms.ModelChoiceField(queryset=Role.objects.filter())
    member=MemberChoiceField(queryset=User.objects.filter())

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
    owner=MemberChoiceField(queryset=User.objects.filter())

    class Meta:
        model = Transaction
        fields = ['owner','bank','txType','exType','remarks','amount','confirmed','date']

    def save(self, commit=True):
        data = super(TransactionForm, self).save(commit=False)
        if commit:
            data.save()

        return data

class TransactionUserForm(forms.ModelForm):
    exType=forms.ModelChoiceField(queryset=ExpenseType.objects.filter())
    class Meta:
        model = Transaction
        fields = ['bank','txType','exType','remarks','amount','date']

    def save(self, commit=True):
        data = super(TransactionUserForm, self).save(commit=False)
        if commit:
            data.save()

        return data

class BankAccountForm(forms.ModelForm):
    holder=MemberChoiceField(queryset=User.objects.filter())
    class Meta:
        model = BankAccount
        fields = ['holder','name','purpose','bank','accNumber','branch','routing','telno','email','balance']

    def save(self, commit=True):
        data = super(BankAccountForm, self).save(commit=False)
        if commit:
            data.save()

        return data

def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == 'member':
        return MemberChoiceField(queryset=User.objects.all())
    
    if db_field.name == 'user':
        return MemberChoiceField(queryset=User.objects.all())

    return super.formfield_for_foreignkey(db_field, request, **kwargs)
