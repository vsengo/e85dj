from django.urls import path,re_path,include
from .views import contributorAddView, contributorListView, contributorDelView, contributorUpdView, constitutionView, reportView
urlpatterns = [
    re_path(r'^contributorList(?P<pk>\d+)', contributorListView, name='contributorList'),
    re_path(r'^contributorAdd(?P<pk>\d+)', contributorAddView, name='contributorAdd'),
    re_path(r'^contributorUpd(?P<pk>\d+)', contributorUpdView, name='contributorUpd'),
    re_path(r'^contributorDel(?P<pk>\d+)', contributorDelView, name='contributorDel'),

    re_path(r'^report(?P<pk>\d+)', reportView, name='report'),
    re_path(r'^constitution', constitutionView, name='constitution'),
]