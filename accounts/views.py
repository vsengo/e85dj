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
from accounts.forms import RegisterForm, MemberForm, ProjectForm, CommiteeForm
from accounts.models import Commitee, Member, Project

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
    form = MemberForm(request.POST or None,instance=member)
    if form.is_valid():
        form.save()
        return redirect('/')

    return render(request = request,template_name = "member.html",context={"form":form})

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
        return render(request = request,template_name = "committee.html",context={"form":form,'project':project})

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
        return render(request = request,template_name = "committee_list.html",context={'committee_list':committees, 'project':project})

class CommitteeUpd(UpdateView):
    model = Commitee
    form_class = CommiteeForm
    template_name = 'committee.html'

    def get_success_url(self):
        return  reverse_lazy('accounts:committeeList', kwargs={'pk':self.object.project_id})

    def get_queryset(self):
        return Commitee.objects.filter(id=self.kwargs['pk'])
 
def committeeUpdSaveView(request,cid,pid):

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
            }
            return render(request,template_name="committee_list.html",context=context)
        else:
            error={'message':'Error'}
            return render(request,template_name='error.html',context=error)

@login_required
def committeeDelView(request,pk):
    committee = Commitee.objects.get(id=pk)
    project = Project.objects.get(id=pid)
    committee.delete()        
    committeeList = Commitee.objects.all().filter(project_id=project.id)
    
    return render(request = request,template_name = "committee_list.html",context={'committee_list':committeeList,'project':project})
