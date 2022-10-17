from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template  import loader
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import UpdateView
from django.contrib  import messages
from django.db import IntegrityError

from django.db.models import Sum, Count
from django.conf import settings
from django.http import JsonResponse
from os import path, rename
from util import img
from PIL import Image
from datetime import datetime
from accounts.forms import RegisterForm, UserForm, MemberForm, ProjectForm, CommiteeForm, MinuteForm, TransactionForm, TransactionUserForm, BankAccountForm
from accounts.models import BankAccount, Commitee, Member, Project, Minute, UserRole, Transaction, ExpenseType, BankAccount

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
                return render(request=request,template_name="error.html", context={'title':"Login ERROR", 'message':"User name <strong>"+username+"</strong> or Password is wrong"})
        else:
            return render(request=request,template_name="error.html", context={'title':"Login ERROR", 'message':"User name or Password is wrong"})

    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

@login_required
def deleteMember(request):
    member = Member.objects.get(user_id=request.user.id)
    user = User.objects.get(id=request.user.id)
    logout(request)
    try:
        user.delete()
    except IntegrityError as e:
        user.is_active=0
        user.username=user.username+"DELETED"
        user.save(update_fields=['is_active'])

    return redirect('/')

@login_required
def memberView(request):
    member = Member.objects.get(user_id=request.user.id)
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        transaction = Transaction.objects.all().filter(owner_id=user.id).order_by('-date')

    return render(request = request,template_name = "member.html",context={'member':member, 'transaction_list':transaction})

@login_required
def memberUpdView(request):
    member = Member.objects.get(user_id=request.user.id)
    user = User.objects.get(id=request.user.id)
    
    if request.method == 'GET':
        profile_form = MemberForm(instance=member)

        user_form = UserForm(instance=user)
        return render(request = request,template_name = "member_upd.html",context={"profile_form":profile_form, 'user_form':user_form, 'member':member})

    if request.method == 'POST':
        member_form = MemberForm(request.POST,request.FILES, instance=request.user.member)
        user_form = UserForm(request.POST,instance=request.user)
        if user_form.is_valid():
            obj=user_form.save(commit=False)
            obj.save(update_fields=['first_name','last_name','email'])

        if member_form.is_valid():
            obj=member_form.save(commit=False)
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
                messages.success(request, "Profile information was updated. Successfully")

        return redirect('accounts:member')

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
        user = User.objects.get(id=request.user.id)

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
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        form = CommiteeForm()
        if project.isCommiteeMember(user) or user.is_staff:
            return render(request = request,template_name = "committee.html",context={"form":form,'project':project})
        else:
            error={'title':'Access Control', 'message':user.first_name+" is not a committee member of "+project.name}
            return render(request,template_name='error.html',context=error)
 
    if request.method == 'POST':
        form = CommiteeForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.updatedBy = user
            obj.project = project
            obj.save()
            committees = Commitee.objects.all().filter(project_id=pk).order_by('role__priority')
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
        committees = Commitee.objects.all().filter(project_id=pk).order_by('role__priority')
        project = Project.objects.get(id=pk)
        user = User.objects.get(id=request.user.id)
        userRole=project.getUserRole(user,'Commitee')

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
    committeeList = Commitee.objects.all().filter(project_id=project.id).order_by('role__priority')
    
    return render(request = request,template_name = "committee_list.html",context={'committee_list':committeeList,'project':project, 'userRole':'EDIT'})

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
            error={'title':'Access Restriction', 'message':user.first_name+" is not a committee member of "+project.name}
            return render(request,template_name='error.html',context=error)
    
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
        minutes = Minute.objects.all().filter(project_id=pk).order_by('-date')
        user = User.objects.get(id=request.user.id)
        prj=Project.objects.get(id=pk)
        userRole=prj.getUserRole(user,'Minute')
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

    minutes = Minute.objects.all().filter(updatedBy=request.user.id).order_by('-date')
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
    userRole=UserRole.EDIT

    minute.delete()     
    minuteList = Minute.objects.all().filter(project_id=project.id)
    
    return render(request = request,template_name = "minute_list.html",context={'minute_list':minuteList,'project':project, 'userRole':userRole})

@login_required
def transactionListView(request, pk):
    prj = Project.objects.all().filter(id=pk).first()
    user = User.objects.get(id=request.user.id)
    
    if request.method == 'GET':

        transactions = Transaction.objects.filter(bank__project__id=pk).order_by('-date')
        userRole = prj.getUserRole(user,'Transaction')
        context={'project':prj, 'transaction_list':transactions, 'userRole':userRole}
        return render(request = request,template_name = "transaction_list.html",context=context)

@login_required
def transactionAddView(request,pk):
    user = User.objects.get(id=request.user.id)
    prj = Project.objects.get(id=pk)
    if request.method == 'GET':
        form = TransactionForm()
        form.fields['exType'].queryset = ExpenseType.objects.filter(prjType_id = prj.prjType.id)
        form.fields['bank'].queryset = BankAccount.objects.filter(project_id=prj.id)
        return render(request = request,template_name = "transaction.html",context={"form":form,'project':prj})
        
    if request.method == 'POST':
        form = TransactionForm(request.POST,request.FILES)

        if form.is_valid():
            try:
                obj=form.save(commit=False)
                obj.updatedBy = user
                obj.save()

                if obj.receipt:
                    today = datetime.now()
                    fname, ext = path.splitext(obj.photo.name)
                    albumPath = path.join(settings.MEDIA_ROOT, "transaction/")
                    opath = path.join(settings.MEDIA_ROOT,fname + ext)
                    nfname = today.strftime("%m%dT%H%M%S") + ext
                    npath = path.join(albumPath,nfname)
                    rename(opath,npath)
                    obj.photo.name = "transaction/"+nfname
                    obj.save(update_fields=['receipt'])

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
    bank = BankAccount.objects.get(id=tx.bank_id)
    project = Project.objects.get(id = bank.project_id)

    if request.method == 'GET':
        form  = TransactionForm(instance = tx)
        return render(request,template_name='common_form.html',context={'form':form, 'form_name':"Transaction "})

    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.updatedBy = user
            obj.project = bank
            obj.id = tx.id
            obj.save()

            if obj.receipt:
                    today = datetime.now()
                    fname, ext = path.splitext(obj.receipt.name)
                    albumPath = path.join(settings.MEDIA_ROOT, "transaction/"+today.strftime("%Y"))
                    opath = path.join(settings.MEDIA_ROOT,fname + ext)
                    nfname = today.strftime("%m%dT%H%M%S") + ext
                    npath = path.join(albumPath,nfname)
                    rename(opath,npath)
                    obj.receipt.name = "transaction/"+today.strftime("%Y")+"/"+nfname
                    obj.save(update_fields=['receipt'])
        else:
            error={'message':'Error in Data input to Minutes'}
            return render(request,template_name='error.html',context=error)

    txs = Transaction.objects.all().filter(bank__project__id=project.id).order_by('-date')
    context ={
        'transaction_list':txs,
        'project':project,
        'userRole':UserRole.EDIT
    }
    return render(request,template_name="transaction_list.html",context=context)

@login_required
def transactionDelView(request,pk):
    tx = Transaction.objects.filter(id=pk).first()
    pid=tx.bank.project_id
    tx.delete()
    transactions = Transaction.objects.all().filter(bank__project__id = pid)
    prj = Project.objects.get(id=pid)
    project = Project.objects.get(id=prj.id)
    return  render(request,template_name="transaction_list.html",context={'transaction_list':transactions,'project':project})

#User Transactions
@login_required
def transactionUserAddView(request):
    return transactionUserView(request,'x')

def transactionUserView(request,pk):
    user = User.objects.get(id=request.user.id)

    if request.method == 'GET':
        if pk == 'x':
            form = TransactionUserForm()
        else:
            tx = Transaction.objects.get(id=pk)
            form = TransactionUserForm(instance=tx)
        return render(request = request,template_name = "common_form.html",context={"form":form, 'form_name':"Transaction"})
        
    if request.method == 'POST':
        form = TransactionUserForm(request.POST,request.FILES)

        if form.is_valid():
            try:
                obj=form.save(commit=False)
                obj.updatedBy = user
                obj.owner_id = user.id
                obj.save()

                if obj.receipt:
                    today = datetime.now()
                    fname, ext = path.splitext(obj.photo.name)
                    albumPath = path.join(settings.MEDIA_ROOT, "transaction/"+today.strftime("%Y"))
                    opath = path.join(settings.MEDIA_ROOT,fname + ext)
                    nfname = today.strftime("%m%dT%H%M%S") + ext
                    npath = path.join(albumPath,nfname)
                    rename(opath,npath)
                    obj.receipt.name = "transaction/"+today.strftime("%Y")+"/"+nfname
                    obj.save(update_fields=['receipt'])

                return redirect('accounts:member') 
            except IntegrityError as e:
                error={'message':'Error'+";".join(e.messages)}
                return render(request,template_name='error.html',context=error)
        else:
            error={'message':'Error'}
            return render(request,template_name='error.html',context=error)

def transactionSummary(request,pk):
    labels = []
    data = []
    queryset = Transaction.objects.all().filter(bank__project__id = pk).values('exType').annotate(total=Sum('amount')).order_by('-exType')

    for entry in queryset:
        exp = ExpenseType.objects.get(id=entry['exType'])
        labels.append(exp.expense)
        data.append(entry['total'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def bankAccountSummary(request,pk):
    labels = []
    data = []
    print("bak account summary")
    queryset = Transaction.objects.all().filter(bank__project__id = pk).filter(txType=Transaction.TxType_DEPOSIT).values('bank_id').annotate(total=Sum('amount'))

    for entry in queryset:
        withdraw = Transaction.objects.all().filter(bank_id =entry['bank_id']).filter(txType=Transaction.TxType_WITHDRWAL).values('bank_id').annotate(total=Sum('amount'))
        if withdraw.count()==0:
            w = 0
        else:
            w = withdraw.first()['total']

        bank = BankAccount.objects.get(id=entry['bank_id'])
        labels.append(bank.name)
        balance = entry['total'] - w
        data.append(balance)
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

@login_required
def bankAccountAddView(request,pk):
    return bankAccountUpdView(request,pk,'x')

@login_required
def bankAccountUpdView(request,pk,bk):
    user = User.objects.get(id=request.user.id)
    prj = Project.objects.get(id=pk)

    if request.method == 'GET':
        if bk=='x':
            form = BankAccountForm()
            bank = BankAccount()
        else:
            bank = BankAccount.objects.get(id=bk) 

        form  = BankAccountForm(instance = bank)
        form_name="Bank Account for "+prj.name  
        return render(request,template_name='common_form.html',context={'form':form, 'form_name':form_name})

    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.updatedBy_id = user.id
            obj.project = prj
            obj.save()
        else:
            error={'message':'Error in Data input to Minutes'}
            return render(request,template_name='error.html',context=error)

        accounts = BankAccount.objects.all().filter(project_id=pk)
        context ={
            'bank_list':accounts,
            'project':prj,
            'userRole':UserRole.EDIT
        }
        return render(request,template_name="bank_list.html",context=context)

@login_required
def bankAccountDelView(request,pk,bk):
    prj = Project.objects.get(id=pk)
    tx = BankAccount.objects.filter(id=bk).first()
    tx.delete()
    banks = BankAccount.objects.all().filter(project_id=pk)
    context ={
            'bank_list':banks,
            'project':prj,
            'userRole':UserRole.EDIT
    }
    return render(request,template_name="bank_list.html",context=context)

@login_required
def bankAccountListView(request, pk):
    prj = Project.objects.all().filter(id=pk).first()
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        banks = BankAccount.objects.all().filter(project_id=prj.id)
        userRole = prj.getUserRole(user,'BankAccount')
        context={'project':prj, 'bank_list':banks, 'userRole':userRole}
        return render(request = request,template_name = "bank_list.html",context=context)

@login_required
def otherPrjListView(request):
    if request.method == 'GET':
        projects = Project.objects.all().exclude(id__in=[1,2])
        for prj in projects:
            txs = Transaction.objects.all().filter(bank__project__id=prj.id)
            raised = txs.filter(txType='DEPOSIT').aggregate(total=Sum('amount'))['total']
            cnt = txs.filter(txType='DEPOSIT').aggregate(cnt=Count('owner'))['cnt']
            spent = txs.filter(txType='WITHDRAWAL').aggregate(total=Sum('amount'))['total']
            prj.raisedFund=raised
            prj.spentFund =spent
            prj.participants=cnt
            prj.save(update_fields=['raisedFund', 'spentFund','participants'])
        
        projects = Project.objects.all().exclude(id__in=[1,2])
        context={'project_list':projects}
        return render(request = request,template_name = "otherprj_list.html",context=context)

@login_required
def financialReport(request, pk):
    prj = Project.objects.get(id=pk)
    templateName='financial_'+str(prj.id)+".html"
    return render(request,template_name=templateName,context={'project':prj})