from django.forms import ModelForm, DateTimeInput
from .models import Task, Project, ProjectMembership


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title']


class TaskFinishedStatusForm(ModelForm):
    class Meta:
        model = Task
        fields = ['finished']


class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date']
        widgets = {'due_date': DateTimeInput(attrs={'placeholder': 'yyyy-mm-dd hh:mm:ss'})}


class ProjectMembershipForm(ModelForm):
    class Meta:
        model = ProjectMembership
        fields = ['user']
