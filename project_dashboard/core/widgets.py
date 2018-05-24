from itertools import chain
from django.contrib.admin import widgets
from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms import Media
from django.forms.widgets import Textarea
from django.utils.encoding import force_text


# Custom forms
class MiniTextarea(Textarea):
    """
    Vertically shorter version of the default Django textarea widget.
    """
    rows = 2

    def __init__(self, attrs=None):
        super(MiniTextarea, self).__init__(
            {'rows': self.rows})


class MiniAdminTextarea(widgets.AdminTextareaWidget):
    """
    Vertically shorter version of the admin textarea widget.
    """
    rows = 2

    def __init__(self, attrs=None):
        super(MiniAdminTextarea, self).__init__(
            {'rows': self.rows})


class MPTTFilteredSelectMultiple(widgets.FilteredSelectMultiple):
    """ MPTT version of FilteredSelectMultiple. """
    option_inherits_attrs = True

    def __init__(self, verbose_name, is_stacked=False, attrs=None, choices=()):
        """ Initializes the widget directly not stacked. """
        super(MPTTFilteredSelectMultiple, self).__init__(
            verbose_name, is_stacked, attrs, choices)

    def optgroups(self, name, value, attrs=None):
        """ Return a list of optgroups for this widget. """
        groups = []
        has_selected = False
        if attrs is None:
            attrs = {}

        for index, (option_value, option_label, sort_fields) in enumerate(
                chain(self.choices)):

            # Set tree attributes
            attrs['data-tree-id'] = sort_fields[0]
            attrs['data-left-value'] = sort_fields[1]

            subgroup = []
            subindex = None
            choices = [(option_value, option_label)]
            groups.append((None, subgroup, index))

            for subvalue, sublabel in choices:
                selected = (
                    force_text(subvalue) in value and
                    (has_selected is False or self.allow_multiple_selected)
                )
                if selected is True and has_selected is False:
                    has_selected = True
                subgroup.append(self.create_option(
                    name, subvalue, sublabel, selected, index,
                    subindex=subindex, attrs=attrs,
                ))

        return groups

    @property
    def media(self):
        """ MPTTFilteredSelectMultiple's Media. """
        js = ['admin/js/core.js',
              'js/mptt_m2m_selectbox.js',
              'admin/js/SelectFilter2.js']
        return Media(js=[staticfiles_storage.url(path) for path in js])
