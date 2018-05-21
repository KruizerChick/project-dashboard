""" Templatetags for Project App """
from django import template
from collections import namedtuple
from itertools import chain

register = template.Library()
Field = namedtuple('Field', 'name verbose_name')
CrudDetail = namedtuple('CrudDetail', ['app', 'model', 'list_url'])


# Crudbuilder templatetags
@register.filter
def class_name(obj):
    return obj.__class__.__name__


@register.filter
def crud_detail(crud_key):
    """ Creates detail arguments for crudbuilder """
    # working, but no URL
    # project, app, model = crud_key.split('-', 4)
    # list_url = '{}-{}-{}-list'.format(project, app, model)
    # return CrudDetail(project, app, model)

    project, app, model = crud_key.split('-', 4)
    list_url = '{}-{}-{}-list'.format(project, app, model)
    return CrudDetail(project, app, model)


@register.filter
def get_model_fields(obj, detail_exclude=None):
    model = obj.__class__
    excludes = ['pk']

    property_fields = []
    for name in dir(model):
        if name not in excludes and isinstance(
            getattr(model, name, None), property
        ):
            property_fields.append(Field(name=name, verbose_name=name))
    fields = chain(obj._meta.fields, property_fields)

    if detail_exclude:
        fields = [field for field in fields if field.name not in detail_exclude]
    return fields
