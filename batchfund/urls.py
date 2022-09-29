from django.urls import path,re_path,include
from .views import contributionAddView, constitutionView
urlpatterns = [
    re_path(r'^contributionAdd', contributionAddView, name='contributionAdd'),
    re_path(r'^constitution', constitutionView, name='constitution'),
]