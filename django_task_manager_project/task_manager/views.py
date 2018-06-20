from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Project, Task, ProjectMembership
from .forms import ProjectForm, TaskUpdateForm, ProjectMembershipForm


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return project_list(request)
    else:
        return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('task_manager:home')


@login_required
def project_view(request, num):
    project = get_object_or_404(Project, id=num)

    if is_user_in_project(request.user, project):
        data = {'project': project}
        return render(request, 'project.html', data)
    else:
        return HttpResponse("No access: this is not your project")


@login_required
def task_view(request, num):
    task = get_object_or_404(Task, id=num)
    if is_user_in_task_project(request.user, task):
        data = {'task': task}
        return render(request, 'task.html', data)
    else:
        return HttpResponse("No access: this task is not yours")


def signup(request):
    if request.user.is_authenticated:
        return redirect('task_manager:home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('task_manager:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def project_form(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('task_manager:project', num=project.pk)
        else:
            raise Http404("Invalid form")
    else:
        form = ProjectForm()
    return render(request, 'project_form.html', {'form': form})


@login_required
def project_list(request):
    projects = Project.objects.filter(Q(user=request.user) | Q(memberships__user=request.user)).distinct()
    return render(request, 'project_list.html', {'projects': projects})


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'task_add.html'
    success_url = reverse_lazy('task_manager:project_list')

    form_class = TaskUpdateForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        project = Project.objects.filter(id=self.kwargs['project'])
        if not project.exists():
            return False

        if is_user_in_project(self.request.user, project[0]):
            form.instance.project = project[0]
            return super().form_valid(form)
        else:
            return False


class ProjectMemberAddView(LoginRequiredMixin, CreateView):
    model = ProjectMembership
    form_class = ProjectMembershipForm
    template_name = 'member_add.html'
    success_url = reverse_lazy('task_manager:project_list')

    def form_valid(self, form):
        form.instance.inviter = self.request.user

        project = Project.objects.filter(id=self.kwargs['project'])
        if not project.exists():
            return False

        if is_user_in_project(self.request.user, project[0]):
            form.instance.project = project[0]
            return super().form_valid(form)
        else:
            return False


@login_required
def task_set_finished(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk)
        if is_user_in_task_project(request.user, task):
            task.finished = True
            task.save()
            previous_page = request.META.get('HTTP_REFERER')
            if previous_page is not None:
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect('task_manager:project_list')
        else:
            return HttpResponse("This task does not belong to one of your projects")
    else:
        previous_page = request.META.get('HTTP_REFERER')
        if previous_page is not None:
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect('task_manager:project_list')


@login_required
def task_remove(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk)
        if is_user_in_task_project(request.user, task):
            task.delete()
            previous_page = request.META.get('HTTP_REFERER')
            if previous_page is not None:
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect('task_manager:project_list')
        else:
            return HttpResponse("This task does not belong to one of your projects")
    else:
        previous_page = request.META.get('HTTP_REFERER')
        if previous_page is not None:
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect('task_manager:project_list')


def is_user_in_task_project(user, task):
    return task.project.user == user or task.project.memberships.filter(user=user).exists()


def is_user_in_project(user, project):
    return project.user == user or project.memberships.filter(user=user).exists()