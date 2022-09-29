from django.urls import re_path
from django.views.generic.base import TemplateView
from .views import ProjectUpd, projectDelView,projectListView,investorAddView, transactionListView, transactionDelView, TransactionUpd, transactionAddView
from .views import financialReport,transactionSummary

urlpatterns = [
    re_path(r'information', TemplateView.as_view(template_name='information.html'), name='information'),
    
    re_path(r'projectList', projectListView, name='projectList'),
    re_path(r'projectDel(?P<pk>\d+)', projectDelView, name='projectDel'),
    re_path(r'projectUpd(?P<pk>\d+)', ProjectUpd.as_view(), name='projectUpd'),
    
    re_path(r'investorAdd', investorAddView, name='investorAdd'),

    re_path(r'transactionList', transactionListView, name='transactionList'),
    re_path(r'transactionAdd(?P<pk>\d+)', transactionAddView, name='transactionAdd'),
    re_path(r'transactionUpd(?P<pk>\d+)', TransactionUpd.as_view(), name='transactionUpd'),
    re_path(r'transactionDel(?P<pk>\d+)', transactionDelView, name='transactionDel'),

    re_path(r'financialReport', financialReport, name='financialReport'),
    re_path(r'transactionSummary',transactionSummary, name='transactionSummary'),

]