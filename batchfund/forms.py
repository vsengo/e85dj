from django import forms
from .models import Contribution
from util.widgets import BootstrapDateTimePickerInput

class ContributeForm(forms.ModelForm):
    widgets = {
            'startDate': BootstrapDateTimePickerInput(format='%Y-%m-%d'), # specify date-frmat
        }
    class Meta:
        model = Contribution
        fields = ('amount','currency','frequency','startDate')
    
    def save(self,commit=True):
        data = super(ContributeForm,self).save(commit=False)
        if commit:
            data.save()
        return data