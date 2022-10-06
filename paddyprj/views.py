from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.template  import loader
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.conf import settings
from django.db import IntegrityError
from accounts.models import Commitee, Project
from .models import PaddyProject, Investor, ProjectStatus, Comment
from .forms import CommentForm, PaddyPrjForm, InvestorForm, ProjectStatusForm, CommentForm
from util import img
from PIL import Image
from datetime import datetime
from os import path, rename

# Create your views here.
@login_required
def projectListView(request):
    if request.method == 'GET':
        #allow only commitee member to update 
        projects = PaddyProject.objects.all()
        return render(request = request,template_name = "paddy_prj_list.html",context={'project_list':projects})

@login_required
def projectDelView(request,pk):
    project = PaddyProject.objects.get(id=pk)
    project.delete()
    projects = Project.objects.all().filter(prjType=Project.PROJ_TYPE_PADDY)
    return render(request = request,template_name = "paddy_prj_list.html",context={'project_list':projects})

class ProjectUpd(UpdateView):
    model = Project
    form_class = PaddyPrjForm
    template_name = 'paddyprj.html'

    def get_success_url(self):
        return  reverse_lazy('paddyprj:projectList')

    def get_queryset(self):
        return PaddyProject.objects.filter(id=self.kwargs['pk'])

@login_required
def investorAddView(request, pk):
    prj=Project.objects.get(id=pk)
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        form = InvestorForm()

        return render(request = request,template_name = "investor.html",context={"form":form, 'project':prj})

    if request.method == 'POST':
        form = InvestorForm(request.POST)
        if form.is_valid():
            try:
                obj=form.save(commit=False)
                obj.user = user
                prj = PaddyProject.objects.get(project_id=pk)
                obj.project = prj
                obj.save()
                return render(request,template_name="investor_success.html",context={'investor':obj,'project':prj})
            except IntegrityError as e:
                error={'message':'Could not save to database'}
                return render(request,template_name='error.html',context=error)
        else:
            error={'message':'Error'}
            return render(request,template_name='error.html',context=error)

@login_required
def investorListView(request, pk):
    prj=Project.objects.get(id=pk)
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        userRole=prj.getUserRole(user)
        paddy=PaddyProject.objects.get(project_id=prj.id)
        status_list = Investor.objects.all().filter(project_id=paddy.id)
        return render(request = request,template_name = "investor_list.html",context={'project':prj, 'status_list':status_list, 'userRole':userRole})

@login_required
def investorUpdView(request,pk):
    user = User.objects.get(id=request.user.id)
    ctx = Investor.objects.get(id=pk)  
    project = Project.objects.get(id=ctx.project_id)
    
    if request.method == 'GET':
        form  = InvestorForm(instance = ctx)
        return render(request,template_name='investor.html',context={'form':form})

    if request.method == 'POST':
        form = InvestorForm(request.POST,request.FILES )
        if form.is_valid():
            obj=form.save(commit=False)
            obj.updatedBy = user
            paddyPrj = PaddyProject.objects.get(project_id = project.id)
            obj.project = paddyPrj
            obj.id = ctx.id
            obj.save()
        else:
            error={'message':'Error in Data input to Minutes'}
            return render(request,template_name='error.html',context=error)

    ctx = Investor.objects.all().filter(project_id=project.id)
    userRole = project.getUserRole(user)

    context ={
        'investor_list':ctx,
        'project':project,
        'userRole':userRole
    }
    return render(request,template_name="investor_list.html",context=context)

@login_required
def investorDelView(request,pk):
    sts = Investor.objects.filter(id=pk).first()
    user = User.get(id=request.user.id)
    pid=sts.project_id
    sts.delete()
    ctx = Investor.objects.all().filter(project_id = pid)
    paddy = PaddyProject.objects.get(id=pid)
    project = Project.objects.get(id=paddy.project_id)
    userRole=project.getUserRole(user)

    context ={
        'investor_list':ctx,
        'project':project,
        'userRole':userRole
    }
    return  render(request,template_name="investor_list.html",context=context)

#Project Status
@login_required
def prjStatusListView(request, pk):
    prj=Project.objects.get(id=pk)
    user = User.objects.get(id=request.user.id)
    if request.method == 'GET':
        userRole=prj.getUserRole(user)
        paddy=PaddyProject.objects.get(project_id=prj.id)
        status_list = ProjectStatus.objects.all().filter(project_id=paddy.id)
        return render(request = request,template_name = "prjstatus_list.html",context={'project':prj, 'status_list':status_list, 'userRole':userRole})

@login_required
def prjStatusAddView(request,pk):
    user = User.objects.get(id=request.user.id)
    prj = Project.objects.get(id=pk)
    if request.method == 'GET':
        form = ProjectStatusForm()
        return render(request = request,template_name = "prjstatus.html",context={"form":form,'project':prj})
    
    if request.method == 'POST':
        form = ProjectStatusForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                obj=form.save(commit=False)
                paddy = PaddyProject.objects.get(project_id=prj.id)
                obj.updatedBy = user
                obj.project = paddy
                obj.save()
                
                if obj.photo:
                    today = datetime.now()
                    twidth, theight = 600, 800
                    fname, ext = path.splitext(obj.photo.name)
                    albumPath = path.join(settings.MEDIA_ROOT, "paddyprj")
                    opath = path.join(settings.MEDIA_ROOT,fname + ext)
                    nfname = today.strftime("%Y") + "/" + today.strftime("%m%dT%H%M%S") + ext
                    npath = path.join(albumPath,nfname)
                    photo = Image.open(opath)
                    width, height = photo.size
                    if (width > twidth):
                        photo = img.apply_orientation(photo)
                        photo.thumbnail((twidth, theight), Image.HAMMING)
                    photo.save(opath)
                    rename(opath,npath)
                    obj.photo.name = "paddyprj/"+nfname
                    obj.save(update_fields=['photo'])

            except IOError as err:
                print("Exception file processing image {0}".format(err))
                pass
            except IntegrityError as e:
                error={'message':'Could not save to database'}
                return render(request,template_name='error.html',context=error)

            return render(request,template_name="prjstatus_success.html",context={'prjStatus':obj,'project':prj})
        else:
            error={'message':'Error'}
            return render(request,template_name='error.html',context=error)
  
@login_required
def prjStatusUpdView(request,pk):
    user = User.objects.get(id=request.user.id)
    ctx = ProjectStatus.objects.get(id=pk)  
    project = Project.objects.get(id=ctx.project_id)
    
    if request.method == 'GET':
        form  = ProjectStatusForm(instance = ctx)
        return render(request,template_name='prjstatus.html',context={'form':form})

    if request.method == 'POST':
        form = ProjectStatusForm(request.POST,request.FILES )
        if form.is_valid():
            obj=form.save(commit=False)
            obj.updatedBy = user
            paddyPrj = PaddyProject.objects.get(project_id = project.id)
            obj.project = paddyPrj
            obj.id = ctx.id
            obj.save()
        else:
            error={'message':'Error in Data input to Minutes'}
            return render(request,template_name='error.html',context=error)

    ctx = ProjectStatus.objects.all().filter(project_id=project.id)
    userRole = project.getUserRole(user)

    context ={
        'prjstatus_list':ctx,
        'project':project,
        'userRole':userRole
    }
    return render(request,template_name="prjstatus_list.html",context=context)

@login_required
def prjStatusDelView(request,pk):
    sts = ProjectStatus.objects.filter(id=pk).first()
    user = User.objects.get(id=request.user.id)
    pid=sts.project_id
    sts.delete()
    status_list = ProjectStatus.objects.all().filter(project_id = pid)
    paddy = PaddyProject.objects.get(id=pid)
    prj = Project.objects.get(id=paddy.project_id)
    userRole=prj.getUserRole(user)

    return  render(request,template_name="prjstatus_list.html",context={'status_list':status_list,'project':prj, 'userRole':userRole})

def statusView(request):
    status_list = ProjectStatus.objects.all()
    return render(request,'status.html', context={'status_list':status_list})

def prjStatusLiked(request, pk):
    obj = get_object_or_404(ProjectStatus, id=pk)
    obj.likes +=1
    obj.save(update_fields=['likes'])
    status_list = ProjectStatus.objects.all()
    return render(request,'status.html', context={'status_list':status_list})

@login_required
def prjStatusComment(request, pk):
    template_name = 'comment_list.html'
    post = get_object_or_404(ProjectStatus, id=pk)
    if post == None:
        return reverse_lazy('paddyprj:prjStatusList')

    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        user = User.objects.get(id=request.user.id)
        
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.status = post
            new_comment.updatedBy = user
            new_comment.save()
            post.comments += 1
            post.save(update_fields=['comments'])

    comment_form = CommentForm()
    comments = Comment.objects.all().filter(status_id=pk)
    return render(request, template_name=template_name, context={'prj': post,
                                           'comment_list': comments,
                                           'form': comment_form})