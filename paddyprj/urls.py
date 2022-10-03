from django.urls import re_path
from django.views.generic.base import TemplateView
from .views import ProjectUpd, projectDelView,projectListView,investorAddView, transactionListView, transactionDelView, TransactionUpd, transactionAddView
from .views import financialReport,transactionSummary, prjStatusDelView, prjStatusAddView, PrjStatusUpd,projectListView, prjStatusListView, statusView
from .views import prjStatusLiked, prjStatusComment

urlpatterns = [
    re_path(r'information', TemplateView.as_view(template_name='information.html'), name='information'),
    re_path(r'status', statusView, name='status'),
    
    re_path(r'projectList', projectListView, name='projectList'),
    re_path(r'projectDel(?P<pk>\d+)', projectDelView, name='projectDel'),
    re_path(r'projectUpd(?P<pk>\d+)', ProjectUpd.as_view(), name='projectUpd'),
    
    re_path(r'investorAdd', investorAddView, name='investorAdd'),

    re_path(r'transactionList', transactionListView, name='transactionList'),
    re_path(r'transactionAdd(?P<pk>\d+)', transactionAddView, name='transactionAdd'),
    re_path(r'transactionUpd(?P<pk>\d+)', TransactionUpd.as_view(), name='transactionUpd'),
    re_path(r'transactionDel(?P<pk>\d+)', transactionDelView, name='transactionDel'),

    re_path(r'prjStatusList', prjStatusListView, name='prjStatusList'),
    re_path(r'prjStatusAdd(?P<pk>\d+)', prjStatusAddView, name='prjStatusAdd'),
    re_path(r'prjStatusUpd(?P<pk>\d+)', PrjStatusUpd.as_view(), name='prjStatusUpd'),
    re_path(r'prjStatusDel(?P<pk>\d+)', prjStatusDelView, name='prjStatusDel'),
    re_path(r'prjStatusLiked(?P<pk>\d+)', prjStatusLiked, name='prjStatusLiked'),
    re_path(r'prjStatusComment(?P<pk>\d+)', prjStatusComment, name='prjStatusComment'),

    re_path(r'financialReport', financialReport, name='financialReport'),
    re_path(r'transactionSummary',transactionSummary, name='transactionSummary'),

]