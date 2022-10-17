from sqlite3 import IntegrityError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.db.models import Sum, Count
from django.http import JsonResponse
from .models import Contribution
from .forms import ContributeForm
from accounts.models import BankAccount, Project, Transaction

@login_required
def contributorAddView(request,pk):
    user = User.objects.get(id=request.user.id)
    prj = Project.objects.get(id=pk)
    if request.method == 'GET':
        form = ContributeForm()
        return render(request = request,template_name = "contribute.html",context={"form":form, 'project':prj})

    if request.method == 'POST':
        form = ContributeForm(request.POST)
        if form.is_valid():
            try:
                obj=form.save(commit=False)
                rec=Contribution.objects.all().filter(project_id = prj.id).filter(user_id=obj.user_id).first()
                if rec:
                    error="User already commited controbution. Please click to update if required"
                    return render(request,template_name='contribution_error.html',context={'error':error,'contribution':rec})

                obj.updatedBy=user
                obj.project = prj
                obj.save()
                contributors = Contribution.objects.all().filter(project_id = prj.id)
                userRole=prj.getUserRole(user,'Contributor')
                ctx={'contributor_list':contributors,'project':prj, 'userRole':userRole}

                return render(request,template_name="contributor_list.html",context=ctx)
            except IntegrityError as e:
                error={'message':'Could not save to database : '}
                return render(request,template_name='error.html',context=error)
        else:
            error={'message':'Error'}
            return render(request,template_name='error.html',context=error)

@login_required
def contributorListView(request, pk):
    prj = Project.objects.get(id=pk)
    user = User.objects.get(id=request.user.id)
    
    if request.method == 'GET':
        contributors = Contribution.objects.all().filter(project_id=prj.id)
        userRole = prj.getUserRole(user,'Contributor')
        form = ContributeForm()
        ctx={"form":form, 'project':prj, 'contributor_list':contributors, 'userRole':userRole}
        return render(request = request,template_name = "contributor_list.html",context=ctx)

@login_required
def contributorUpdView(request,pk):
    user = User.objects.get(id=request.user.id)
    ctx = Contribution.objects.get(id=pk)  
    project = Project.objects.get(id=ctx.project_id)
    
    if request.method == 'GET':
        form  = ContributeForm(instance = ctx)
        return render(request,template_name='contribute.html',context={'form':form})

    if request.method == 'POST':
        form = ContributeForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.updatedBy = user
            obj.project = project
            obj.id = ctx.id
            obj.save()
        else:
            error={'message':'Error in Data input to Minutes'}
            return render(request,template_name='error.html',context=error)

    ctx = Contribution.objects.all().filter(project_id=project.id)
    userRole = project.getUserRole(user,'Contributor')

    context ={
        'contributor_list':ctx,
        'project':project,
        'userRole':userRole
    }
    return render(request,template_name="contributor_list.html",context=context)

@login_required
def contributorDelView(request,pk):
    tx = Contribution.objects.filter(id=pk).first()
    pid=tx.project_id
    tx.delete()
    contributors = Contribution.objects.all().filter(project_id = pid)
    prj = Project.objects.get(id=pid)
    user = User.objects.get(id=request.user.id)
    userRole=prj.getUserRole(user,'Contributor')
    ctx={'contributor_list':contributors,'project':prj, 'userRole':userRole}
    return  render(request,template_name="contributor_list.html",context=ctx)


def constitutionView(request):
    if request.method == 'GET':
        return render(request = request,template_name = "constitution.html")

def reportView(request,pk):
    prj = Project.objects.get(id=pk)
    cns = Contribution.objects.all().filter(project_id=pk)
    cns_count=cns.count()
    cns_total = cns.aggregate(total=Sum('amount'))
    freq_sum = Contribution.objects.values('frequency').annotate(Sum('amount')).annotate(cnt=Count('frequency'))  
    freq_cnt = cns.annotate(Count('frequency')) 
    freq_list=freq_sum
    
    txs = Transaction.objects.all().filter(bank__project__id=pk).filter(txType='DEPOSIT')
    tx_count=txs.count()
    tx_total = txs.aggregate(total=Sum('amount'))


    ctx = {'contrib_count':cns_count,'contrib_total':cns_total['total'],'freq_list':freq_list,
            'tx_count':tx_count,'tx_total':tx_total['total'],
            'project':prj}
    if request.method == 'GET':
        return render(request=request,template_name="report.html",context = ctx)

