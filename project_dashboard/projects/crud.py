""" CRUD class for Projects app """
from crudbuilder.abstract import BaseCrudBuilder

from .models import Project


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
