""" Template tags and filters for Projects """
from django.template import Library

from ..models import Project

register = Library()


# Templatetags
@register.inclusion_tag('projects/tags/dummy.html', takes_context=True)
def get_projects(context, template='projects/tags/projects.html'):
    """ Return all projects. """
    return {'template': template,
            'projects': Project.objects.all(),
            'context_project': context.get('project')}
