""" Template tags and filters for Projects """
from django.db.models import Count
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


@register.inclusion_tag('projects/tags/dummy.html', takes_context=True)
def get_open_projects(context, template='projects/tags/projects.html'):
    """ Return only open projects. """
    return {'template': template,
            'projects': Project.open_projects.all().annotate(
                no_of_projects=Count('name')),
            'context_project': context.get('project')}
