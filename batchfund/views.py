from sqlite3 import IntegrityError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Contribution, ContributionHist
from .forms import ContributeForm
from accounts.models import Project

@login_required
def contributionAddView(request):
    if request.method == 'GET':
        form = ContributeForm()
        prj = Project.objects.all().filter(prjType=Project.PROJ_TYPE_CHARITY).first()
        return render(request = request,template_name = "contribute.html",context={"form":form, 'project':prj})

    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        form = ContributeForm(request.POST)

        if form.is_valid():
            try:
                obj=form.save(commit=False)
                obj.user = user
                prj = Project.objects.get(id=1)
                obj.project = prj
                obj.save()
                return render(request,template_name="contribution_success.html",context={'contribution':obj,'project':prj})
            except IntegrityError as e:
                error={'message':'Could not save to database'}
                return render(request,template_name='error.html',context=error)
        else:
            error={'message':'Error'}
            return render(request,template_name='error.html',context=error)

def constitutionView(request):
    if request.method == 'GET':
        return render(request = request,template_name = "constitution.html")