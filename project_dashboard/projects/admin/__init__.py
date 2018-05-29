""" Admin of Projects app """

from django.contrib import admin

from .project import ProjectAdmin
# from .stakeholder import RoleAdmin
from .stakeholder import StakeholderAdmin, RoleAdmin
from .issue import IssueAdmin
from .category import CategoryAdmin
from .task import TaskAdmin

from .. import models as proj_models


admin.site.register(proj_models.Project, ProjectAdmin)
admin.site.register(proj_models.Membership)
admin.site.register(proj_models.Stakeholder, StakeholderAdmin)
admin.site.register(proj_models.Role, RoleAdmin)
admin.site.register(proj_models.Task, TaskAdmin)
admin.site.register(proj_models.Issue, IssueAdmin)
admin.site.register(proj_models.Category, CategoryAdmin)
