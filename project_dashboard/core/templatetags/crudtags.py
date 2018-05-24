""" Crudbuilder Templatetags for Project Dashboard """
# Original crudbuilder templatetags weren't working right with the
# modular configuration of this project.
# (app.model is the standard for crudbuilder, not project.app.model)

from django import template
from collections import namedtuple
from itertools import chain

register = template.Library()
Field = namedtuple('Field', 'name verbose_name')
CrudDetail = namedtuple('CrudDetail', ['module', 'app', 'model', 'list_url'])


# Crudbuilder templatetags
@register.filter
def class_name(obj):
    return obj.__class__.__name__


@register.filter
def crud_detail(crud_key):
    """ Creates detail arguments for crudbuilder """
    # working, but no URL
    module, app, model = crud_key.split('-', 4)
    list_url = '{}-{}-{}-list'.format(module, app, model)
    return CrudDetail(module, app, model, list_url)


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
