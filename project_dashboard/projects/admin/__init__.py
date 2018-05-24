""" Admin of Projects app """

from django.contrib import admin

from .project import ProjectAdmin
# from .stakeholder import RoleAdmin
from .stakeholder import StakeholderAdmin

from ..models.project import Project
from ..models.stakeholder import Stakeholder
from ..models.task import Task


admin.site.register(Project, ProjectAdmin)
admin.site.register(Stakeholder, StakeholderAdmin)
admin.site.register(Task)
