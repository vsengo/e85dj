from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,re_path,include
from .views import  SignUpView, logOff, logIn, memberView, projectAddView,projectListView,projectDelView,ProjectUpd
from .views import committeeAddView, CommitteeUpd, committeeDelView,committeeListView, minuteAddView, minuteDelView, minuteListView, minuteUpdView

urlpatterns = [
    re_path(r'signup', SignUpView.as_view(), name='signup'),
    re_path(r'logoff', logOff, name='logoff'),
    re_path(r'login', logIn, name='login'),
    re_path(r'^member', memberView, name='member'),

    re_path(r'projectList', projectListView, name='projectList'),
    re_path(r'projectAdd', projectAddView, name='projectAdd'),
    re_path(r'projectDel(?P<pk>\d+)', projectDelView, name='projectDel'),
    re_path(r'projectUpd(?P<pk>\d+)', ProjectUpd.as_view(), name='projectUpd'),

    re_path(r'committeeList(?P<pk>\d+)', committeeListView, name='committeeList'),
    re_path(r'committeeAdd(?P<pk>\d+)', committeeAddView, name='committeeAdd'),
    re_path(r'committeeDel(?P<pk>\d+)', committeeDelView, name='committeeDel'),
    re_path(r'committeeUpd(?P<pk>\d+)', CommitteeUpd.as_view(), name='committeeUpd'),
    
    re_path(r'minuteList(?P<pk>\d+)', minuteListView, name='minuteList'),
    re_path(r'minuteAdd(?P<pk>\d+)', minuteAddView, name='minuteAdd'),
    re_path(r'minuteDel(?P<pk>\d+)', minuteDelView, name='minuteDel'),
    re_path(r'minuteUpd(?P<pk>\d+)', minuteUpdView, name='minuteUpd'),

    re_path(r'password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset/pwdreset_form.html',
             subject_template_name='accounts/password_reset/pwdreset_subject.txt',
             email_template_name='accounts/password_reset/pwdreset_email.html',
             success_url='login'
         ),
         name='password_reset'),
    
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset/pwdreset_confirm.html'),
         name='password_reset_confirm'),

    path('password_reset_complete$',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset/pwdreset_complete.html'),
         name='password_reset_complete'),
]