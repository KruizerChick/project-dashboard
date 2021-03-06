from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    # path('', views.project_list, name='list'),
    path('list', views.open_projects, name='list'),
    path('add', views.ProjectCreateView.as_view(), name='add'),
    path('<slug:project_slug>', views.project_detail, name='detail'),

]
