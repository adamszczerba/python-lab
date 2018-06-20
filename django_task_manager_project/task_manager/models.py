from django.db import models
from django.contrib.auth.models import User


# Projekt, w wamach którego będą wyznaczane zadania do wykonania.
class Project(models.Model):
    title = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)


# Zadanie do wykonania
class Task(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    priority = models.IntegerField(default=1, choices=((1, 1),(2, 2),(3, 3),(4, 4),(5, 5)))
    due_date = models.DateTimeField(blank=True, null=True, default=None)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

    finished = models.BooleanField(default=False)
    finished_date = models.DateTimeField(blank=True, null=True, default=None)
    finisher = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE, related_name="+")  # Osoba, która zakończyła task'a

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        str_template = "Task: {}\nDescription: {}\nPriority: {}\n" + \
                       "Due to: {}\nCreated by: {}\nFrom project: {}\nIs done: {}\n"
        return str_template.format(self.title, self.description, self.priority, self.due_date,
                                   self.creator, self.project, self.finished)

    def task_finished_status_form(self):
        from .forms import TaskFinishedStatusForm
        return TaskFinishedStatusForm(instance=self)


# Model opisujący członkostwo w projekcie.
class ProjectMembership(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_memberships")
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")


