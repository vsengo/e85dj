from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from django.template  import loader
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.conf import settings
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
def investorAddView(request):
    if request.method == 'GET':
        form = InvestorForm()
        prj = Project.objects.all().filter(prjType=Project.PROJ_TYPE_PADDY).first()
        return render(request = request,template_name = "investor.html",context={"form":form, 'project':prj})

    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        form = InvestorForm(request.POST)

        if form.is_valid():
            try:
                obj=form.save(commit=False)
                obj.user = user
                prj = Project.objects.all().filter(prjType=Project.PROJ_TYPE_PADDY).first()
                obj.project = prj
                obj.save()
                return render(request,template_name="investor_success.html",context={'investor':obj,'project':prj})
            except IntegrityError as e:
                error={'message':'Could not save to database'}
                return render(request,template_name='error.html',context=error)
        else:
            error={'message':'Error'}
            return render(request,template_name='error.html',context=error)

#Project Status
@login_required
def prjStatusListView(request):
    if request.method == 'GET':
        prj = Project.objects.all().filter(prjType=Project.PROJ_TYPE_PADDY).first()
        user = User.objects.get(id=request.user.id)

        if prj.isCommiteeMember(user):
            paddy=PaddyProject.objects.get(project_id=prj.id)
            status_list = ProjectStatus.objects.all().filter(project_id=paddy.id)
            return render(request = request,template_name = "prjstatus_list.html",context={'project':prj, 'status_list':status_list})
        else:
            error={'message':user.first_name+" is not a committee member of "+prj.name}
            return render(request,template_name='accessControl.html',context=error)

    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        form = ProjectStatusForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                obj=form.save(commit=False)
                prj = Project.objects.all().filter(proj_type=Project.PROJ_TYPE_PADDY)
                paddy = PaddyProject.objects.get(project_id=prj.id)
                obj.updatedBy = user
                obj.project = paddy
                obj.save()
                return render(request,template_name="prjstatus_success.html",context={'prjstatus':obj,'project':prj})
            except IntegrityError as e:
                error={'message':'Could not save Project status to database'}
                return render(request,template_name='error.html',context=error)
        else:
            error={'message':'Error'}
            return render(request,template_name='error.html',context=error)

@login_required
def prjStatusAddView(request,pk):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        prj = Project.objects.get(id=pk)
        if prj.isCommiteeMember(user):
            paddy=PaddyProject.objects.get(project_id=prj.id)
            form = ProjectStatusForm()
            return render(request = request,template_name = "prjstatus.html",context={"form":form,'project':prj})
        else:
            error={'message':user.first_name+" is not a committee member of "+prj.name}
            return render(request,template_name='accessControl.html',context=error)
       

    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        form = ProjectStatusForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                obj=form.save(commit=False)
                prj = Project.objects.all().filter(prjType=Project.PROJ_TYPE_PADDY).first()
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
                    #obj.save(update_fields=["photo"])
                    print("Saved news Pic opath = "+opath)
                    print("Saved in npath="+npath+" nfname="+nfname)

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
  
        
  
class PrjStatusUpd(UpdateView):
    model = ProjectStatus
    form_class = ProjectStatusForm
    template_name = 'prjstatus.html'

    def get_success_url(self):
        return  reverse_lazy('paddyprj:prjStatusList')

    def get_queryset(self):
        return ProjectStatus.objects.filter(id=self.kwargs['pk'])

@login_required
def prjStatusDelView(request,pk):
    sts = ProjectStatus.objects.filter(id=pk).first()
    pid=sts.project_id
    sts.delete()
    status_list = ProjectStatus.objects.all().filter(project_id = pid)
    paddy = PaddyProject.objects.get(id=pid)
    prj = Project.objects.get(id=paddy.project_id)
    return  render(request,template_name="prjstatus_list.html",context={'status_list':status_list,'project':prj})

def statusView(request):
    status_list = ProjectStatus.objects.all()

    return render(request,'status.html', context={'status_list':status_list})


#Project Status
@login_required
def prjStatusListView(request):
    if request.method == 'GET':
        prj = Project.objects.all().filter(prjType=Project.PROJ_TYPE_PADDY).first()
        user = User.objects.get(id=request.user.id)

        if prj.isCommiteeMember(user):
            paddy=PaddyProject.objects.get(project_id=prj.id)
            status_list = ProjectStatus.objects.all().filter(project_id=paddy.id)
            return render(request = request,template_name = "prjstatus_list.html",context={'project':prj, 'status_list':status_list})
        else:
            error={'message':user.first_name+" is not a committee member of "+prj.name}
            return render(request,template_name='accessControl.html',context=error)

    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        form = ProjectStatusForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                obj=form.save(commit=False)
                prj = Project.objects.all().filter(proj_type=Project.PROJ_TYPE_PADDY)
                paddy = PaddyProject.objects.get(project_id=prj.id)
                obj.updatedBy = user
                obj.project = paddy
                obj.save()
                return render(request,template_name="prjstatus_success.html",context={'prjstatus':obj,'project':prj})
            except IntegrityError as e:
                error={'message':'Could not save Project status to database'}
                return render(request,template_name='error.html',context=error)
        else:
            error={'message':'Error'}
            return render(request,template_name='error.html',context=error)

@login_required
def prjStatusAddView(request,pk):
    if request.method == 'GET':
        form = ProjectStatusForm()
        prj = Project.objects.get(id=pk)
        return render(request = request,template_name = "prjstatus.html",context={"form":form,'project':prj})

    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        form = ProjectStatusForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                obj=form.save(commit=False)
                prj = Project.objects.all().filter(prjType=Project.PROJ_TYPE_PADDY).first()
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