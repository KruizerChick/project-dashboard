from django.contrib import admin
from django.urls import path

from . import views

app_name = 'project'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('add', views.ProjectCreateView.as_view(), name='add'),
    path('<slug:project_slug>', views.project_detail, name='detail'),

]
