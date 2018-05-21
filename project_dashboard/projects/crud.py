""" CRUD class for Projects app """
from crudbuilder.abstract import BaseCrudBuilder

from .models import Project, Stakeholder


class ProjectCrud(BaseCrudBuilder):
    """ CRUD class for Project model """
    model = Project
    search_fields = ["id", "name", "description", ]
    tables2_fields = ("name", "description")
    tables2_css_class = "table table-bordered table-condensed"
    login_required = True
    permission_required = True
    # tables2_pagination = 20  # default is 10
    # modelform_excludes = ['date_created']

    # permissions = {}
    # custom_templates = {}


class StakeholderCrud(BaseCrudBuilder):
    """ CRUD class for Stakeholder model """
    model = Stakeholder
    search_fields = ["full_name", ]
    tables2_fields = ("full_name", "organization")
    tables2_css_class = "table table-bordered table-condensed"

    login_required = True
    permission_required = True
#     # tables2_pagination = 20  # default is 10
#     # modelform_excludes = ['date_created']

#     # permissions = {}
#     # custom_templates = {}
