from django.urls import re_path
from . import views

app_name = 'home'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='Home'),
]
