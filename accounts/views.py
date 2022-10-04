from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template  import loader
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import UpdateView
from django.contrib  import messages
from django.db import IntegrityError
from django.db.models import Sum
from django.conf import settings
from django.http import JsonResponse
from os import path, rename
from util import img
from PIL import Image
from datetime import datetime
from accounts.forms import RegisterForm, MemberForm, ProjectForm, CommiteeForm, MinuteForm, TransactionForm
from accounts.models import Commitee, Member, Project, Minute, UserRole, Transaction, ExpenseType

class SignUpView(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'signup.html'

def logIn(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                c =  {'user_id':user.id,
                     'name':user.first_name
                     }
                t = loader.get_template('home/base.html')
                #request.user = user
                return  render(request = request,template_name = "home/index.html",context=c)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})

@login_required
def memberView(request):
    member = Member.objects.get(user_id=request.user.id)
    if request.method == 'GET':
        form = MemberForm(instance=member)
        return render(request = request,template_name = "member.html",context={"form":form, 'member':member})
        
    if request.method == 'POST':
        form = MemberForm(request.POST,request.FILES)
        if form.is_valid():
            obj=form.save(commit=False)
            user = User.objects.get(id=request.user.id)
            obj.user = user
            obj.id=member.id
            obj.save()
            
            if obj.photo:
                today = datetime.now()
                twidth, theight = 150, 200
                fname, ext = path.splitext(obj.photo.name)
                albumPath = path.join(settings.MEDIA_ROOT, "profile/")
                opath = path.join(settings.MEDIA_ROOT,fname + ext)
                nfname = today.strftime("%m%dT%H%M%S") + ext
                npath = path.join(albumPath,nfname)
                photo = Image.open(opath)
                width, height = photo.size
                if (width > twidth):
                    photo = img.apply_orientation(photo)
                    photo.thumbnail((twidth, theight), Image.HAMMING)
                photo.save(opath)
                rename(opath,npath)
                obj.photo.name = "profile/"+nfname
                obj.save()

        return redirect('/')

@login_required
def logOff(request):
    logout(request)
    user = User.objects.filter(username=request.user)
    return render(request, 'logoff.html',{'user':user})

@login_required
def projectAddView(request):
    if request.method == 'GET':
        form = ProjectForm()
        return render(request = request,template_name = "project.html",context={"form":form})

    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        form = ProjectForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.updatedBy = user
            obj.save()
            projects = Project.objects.all().filter(updatedBy=request.user.id)
            return render(request,template_name="project_list.html",context={'project_list':projects})
        else:
            error={'message':'Error'}
            return render(request,template_name='error.html',context=error)

@login_required
def projectListView(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        return render(request = request,template_name = "project_list.html",context={'project_list':projects})

@login_required
def projectDelView(request,pk):
    project = Project.objects.get(id=pk)
    project.delete()
    projects= Project.objects.all().filter(updatedBy=request.user.id)
    return render(request = request,template_name = "project_list.html",context={'project_list':projects})

class ProjectUpd(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project.html'

    def get_success_url(self):
        return  reverse_lazy('accounts:projectList')

    def get_queryset(self):
        return Project.objects.filter(id=self.kwargs['pk'])


@login_required
def committeeAddView(request,pk):
    project = Project.objects.get(id=pk)

    if request.method == 'GET':
        form = CommiteeForm()
        if project.isCommiteeMember(user):
            form = MinuteForm()
            return render(request = request,template_name = "committee.html",context={"form":form,'project':project})
        else:
            error={'message':user.first_name+" is not a committee member of "+project.name}
            return render(request,template_name='accessControl.html',context=error)
 
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)

        form = CommiteeForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.updatedBy = user
            obj.project = project
            obj.save()
            committees = Commitee.objects.all().filter(updatedBy=request.user.id)
            context ={
                'committee_list':committees,
                'project':project,
                'userRole':'EDIT'
            }
            return render(request,template_name="committee_list.html",context=context)
        else:
            error={'message':'Error'}
            return render(request,template_name='error.html',context=error)

@login_required
def committeeListView(request,pk):
    if request.method == 'GET':
        committees = Commitee.objects.all().filter(project_id=pk)
        project = Project.objects.get(id=pk)
        user = User.objects.get(id=request.user.id)
        userRole = UserRole.VIEW
        userRole=UserRole.VIEW
        if project.isCommiteeMember(user):
            userROle=UserRole.EDIT

        return render(request = request,template_name = "committee_list.html",context={'committee_list':committees, 'project':project, 'userRole':userRole})

class CommitteeUpd(UpdateView):
    model = Commitee
    form_class = CommiteeForm
    template_name = 'committee.html'

    def get_success_url(self):
        return  reverse_lazy('accounts:committeeList', kwargs={'pk':self.object.project_id})

    def get_queryset(self):
        return Commitee.objects.filter(id=self.kwargs['pk'])
 
@login_required
def committeeDelView(request,pk):
    committee = Commitee.objects.get(id=pk)
    project = Project.objects.get(id=committee.project_id)
    committee.delete()        
    committeeList = Commitee.objects.all().filter(project_id=project.id)
    
    return render(request = request,template_name = "committee_list.html",context={'committee_list':committeeList,'project':project})

#Minutes
@login_required
def minuteAddView(request,pk):
    project = Project.objects.get(id=pk)
    user = User.objects.get(id=request.user.id)  
    
    if request.method == 'GET':
        if project.isCommiteeMember(user):
            form = MinuteForm()
            return render(request = request,template_name = "minute.html",context={"form":form,'project':project})
        else:
            error={'message':user.first_name+" is not a committee member of "+project.name}
            return render(request,template_name='accessControl.html',context=error)
    
    if request.method == 'POST':
        form = MinuteForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.updatedBy = user
            obj.project = project
            obj.save()
            minutes = Minute.objects.all().filter(updatedBy=request.user.id)
            context ={
                'minute_list':minutes,
                'project':project,
            }
            return render(request,template_name="minute_list.html",context=context)
        else:
            error={'message':'Error in Data input to Minutes'}
            return render(request,template_name='error.html',context=error)

@login_required
def minuteListView(request,pk):
    if request.method == 'GET':
        minutes = Minute.objects.all().filter(project_id=pk)
        user = User.objects.get(id=request.user.id)
        prj=Project.objects.get(id=pk)
        userRole = UserRole.VIEW
        if prj.isCommiteeMember(user):
            userRole=UserRole.EDIT

        return render(request = request,template_name = "minute_list.html",context={'minute_list':minutes, 'userRole':userRole, 'project':prj})

class MinuteUpd(UpdateView):
    model = Minute
    form_class = MinuteForm
    template_name = 'minute.html'

    def get_success_url(self):
        return  reverse_lazy('accounts:minuteList', kwargs=self.kwargs['pk'])

    def get_queryset(self):
        return Minute.objects.filter(id=self.kwargs['pk'])

def minuteUpdView(request,pk):
    user = User.objects.get(id=request.user.id)
    minute = Minute.objects.get(id=pk)  
    project = Project.objects.get(id=minute.project_id)
    
    if request.method == 'GET':
        form  = MinuteForm(instance = minute)
        return render(request,template_name='minute.html',context={'form':form})

    if request.method == 'POST':
        form = MinuteForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.updatedBy = user
            obj.project = project
            obj.id = minute.id
            obj.save()

        else:
            error={'message':'Error in Data input to Minutes'}
            return render(request,template_name='error.html',context=error)

    minutes = Minute.objects.all().filter(updatedBy=request.user.id)
    context ={
        'minute_list':minutes,
        'project':project,
        'userRole':UserRole.EDIT
    }
    return render(request,template_name="minute_list.html",context=context)

@login_required
def minuteDelView(request,pk):
    minute = Minute.objects.get(id=pk)
    user = User.objects.get(id=request.user.id)
    project=Project.objects.get(id=minute.project_id)
    userRole = UserRole.VIEW   
    if project.isCommiteeMember(user):
        userRole=UserRole.EDIT

    minute.delete()     
    minuteList = Minute.objects.all().filter(project_id=project.id)
    
    return render(request = request,template_name = "minute_list.html",context={'minute_list':minuteList,'project':project, 'userRole':userRole})

@login_required
def transactionListView(request, pk):
    prj = Project.objects.all().filter(id=pk).first()
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        transactions = Transaction.objects.all().filter(project_id=prj.id)
        userRole = prj.getUserRole(user)
        context={'project':prj, 'transaction_list':transactions, 'userRole':userRole}
        return render(request = request,template_name = "transaction_list.html",context=context)
@login_required
def transactionAddView(request,pk):
    user = User.objects.get(id=request.user.id)
    prj = Project.objects.get(id=pk)
    if request.method == 'GET':
        if prj.isCommiteeMember(user):
            form = TransactionForm()
            return render(request = request,template_name = "transaction.html",context={"form":form,'project':prj})
        else:
            error={'message':user.first_name+" is not a committee member of "+prj.name}
            return render(request,template_name='accessControl.html',context=error)
        
    if request.method == 'POST':
        form = TransactionForm(request.POST,request.FILES)

        if form.is_valid():
            try:
                obj=form.save(commit=False)
                obj.updatedBy = user
                obj.project = prj
                obj.save()
                return render(request,template_name="transaction_success.html",context={'transaction':obj,'project':prj})
            except IntegrityError as e:
                error={'message':'Could not save to database'}
                return render(request,template_name='error.html',context=error)
        else:
            error={'message':'Error'}
            return render(request,template_name='error.html',context=error)

@login_required
def transactionUpdView(request,pk):
    user = User.objects.get(id=request.user.id)
    tx = Transaction.objects.get(id=pk)  
    project = Project.objects.get(id=tx.project_id)
    
    if request.method == 'GET':
        form  = TransactionForm(instance = tx)
        return render(request,template_name='transaction.html',context={'form':form})

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.updatedBy = user
            obj.project = project
            obj.id = tx.id
            obj.save()

        else:
            error={'message':'Error in Data input to Minutes'}
            return render(request,template_name='error.html',context=error)

    txs = Transaction.objects.all().filter(project_id=tx.project_id)
    context ={
        'transaction_list':txs,
        'project':project,
        'userRole':UserRole.EDIT
    }
    return render(request,template_name="transaction_list.html",context=context)

@login_required
def transactionDelView(request,pk):
    tx = Transaction.objects.filter(id=pk).first()
    pid=tx.project_id
    tx.delete()
    transactions = Transaction.objects.all().filter(project_id = pid)
    prj = Project.objects.get(id=pid)
    project = Project.objects.get(id=prj.id)
    return  render(request,template_name="transaction_list.html",context={'transaction_list':transactions,'project':project})


def transactionSummary(request,pk):
    labels = []
    data = []

    queryset = Transaction.objects.all().filter(project_id=pk).values('exType').annotate(total=Sum('amount')).order_by('-exType')

    for entry in queryset:
        exp = ExpenseType.objects.get(id=entry['exType'])
        labels.append(exp.expense)
        data.append(entry['total'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

@login_required
def financialReport(request, pk):
    prj = Project.objects.get(id=pk)
    templateName='financial_'+str(prj.id)+".html"
    return render(request,template_name=templateName,context={'project':prj})