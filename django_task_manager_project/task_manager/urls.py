from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views
from django.http import HttpResponse


app_name = 'task_manager'

urlpatterns = [
    path(r'', views.index, name='home'),
    path(r'login/', auth_views.login, name='login'),
    path(r'logout/', views.logout_view, name='logout'),
    path(r'signup/', views.signup, name='signup'),
    path(r'project/<int:num>', views.project_view, name='project'),
    path(r'task/<int:num>', views.task_view, name='task'),
    path(r'project/list/', views.project_list, name='project_list'),
    path(r'project/add/', views.project_form, name='project_add'),
    path(r'task/<int:pk>/finished', views.task_set_finished, name='task_set_finished'),
    path(r'task/<int:pk>/remove', views.task_remove, name='task_remove'),
    path(r'task/add/<int:project>', views.TaskCreateView.as_view(), name="task_add"),
    path(r'project/<int:project>/member_add', views.ProjectMemberAddView.as_view(), name='member_add')
]

