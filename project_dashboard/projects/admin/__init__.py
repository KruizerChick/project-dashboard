""" Admin of Projects app """

from django.contrib import admin

from .project import ProjectAdmin
# from .stakeholder import RoleAdmin
from .stakeholder import StakeholderAdmin
from .issue import IssueAdmin
from .category import CategoryAdmin

from .. import models as proj_models
# from ..models.project import Project
# from ..models.stakeholder import Stakeholder
# from ..models.task import Task
# from ..models.issue import Issue


admin.site.register(proj_models.Project, ProjectAdmin)
admin.site.register(proj_models.Stakeholder, StakeholderAdmin)
admin.site.register(proj_models.Task)
admin.site.register(proj_models.Issue, IssueAdmin)
admin.site.register(proj_models.Category, CategoryAdmin)
