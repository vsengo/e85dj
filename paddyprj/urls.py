from django.urls import re_path
from django.views.generic.base import TemplateView
from .views import ProjectUpd, projectDelView,projectListView,investorAddView
from .views import prjStatusDelView, prjStatusAddView, prjStatusUpdView,projectListView, prjStatusListView, statusView
from .views import prjStatusLiked, prjStatusComment, investorDelView, investorListView, investorUpdView

urlpatterns = [
    re_path(r'information', TemplateView.as_view(template_name='information.html'), name='information'),
    re_path(r'status', statusView, name='status'),
    
    re_path(r'prjtList', projectListView, name='prjList'),
    re_path(r'prjtDel(?P<pk>\d+)', projectDelView, name='prjDel'),
    re_path(r'prjtUpd(?P<pk>\d+)', ProjectUpd.as_view(), name='prjUpd'),
    
    re_path(r'investorAdd(?P<pk>\d+)',   investorAddView, name='investorAdd'),
    re_path(r'investorList(?P<pk>\d+)', investorListView, name='investorList'),
    re_path(r'investorUpd(?P<pk>\d+)',  investorUpdView, name='investorUpd'),
    re_path(r'investorDel(?P<pk>\d+)',  investorDelView, name='investorDel'),

    re_path(r'prjStatusList(?P<pk>\d+)', prjStatusListView, name='prjStatusList'),
    re_path(r'prjStatusAdd(?P<pk>\d+)', prjStatusAddView, name='prjStatusAdd'),
    re_path(r'prjStatusUpd(?P<pk>\d+)', prjStatusUpdView, name='prjStatusUpd'),
    re_path(r'prjStatusDel(?P<pk>\d+)', prjStatusDelView, name='prjStatusDel'),

    re_path(r'prjStatusLiked(?P<pk>\d+)', prjStatusLiked, name='prjStatusLiked'),
    re_path(r'prjStatusComment(?P<pk>\d+)', prjStatusComment, name='prjStatusComment'),
]