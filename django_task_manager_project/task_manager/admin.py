from django.contrib import admin
from .models import *


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    pass


class TaskAdmin(admin.ModelAdmin):
    pass


class ProjectMembershipAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(ProjectMembership, ProjectMembershipAdmin)
