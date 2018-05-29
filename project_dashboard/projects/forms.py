from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.utils.translation import ugettext_lazy as _

from mptt.forms import TreeNodeChoiceField

from ..core.fields import MPTTModelMultipleChoiceField
# from ..core.fields import MPTTModelChoiceIterator
from ..core.widgets import MiniAdminTextarea, MPTTFilteredSelectMultiple

from . import models as proj_models


# App forms
class ExpenseForm(forms.Form):
    title = forms.CharField()
    amount = forms.IntegerField()
    category = forms.CharField()


class IssueAdminForm(forms.ModelForm):
    """ Dependent dropdown form limiting tasks to selected project """
    categories = MPTTModelMultipleChoiceField(
        label=_('Categories'), required=False,
        queryset=proj_models.Category.objects.all(),
        widget=MPTTFilteredSelectMultiple(_('categories')))

    def __init__(self, *args, **kwargs):
        super(IssueAdminForm, self).__init__(*args, **kwargs)
        self.fields['task'].queryset = proj_models.Task.objects.none()
        self.fields['categories'].widget = RelatedFieldWidgetWrapper(
            self.fields['categories'].widget,
            proj_models.Issue.category.field.remote_field,
            self.admin_site)

    class Meta:
        model = proj_models.Issue
        fields = '__all__'
        widgets = {
            'description': MiniAdminTextarea,
            'impact': MiniAdminTextarea,
            'resolution_plan': MiniAdminTextarea,
        }


class CategoryAdminForm(forms.ModelForm):
    """ Form for Category's Admin. """
    parent = TreeNodeChoiceField(
        label=_('Parent category'),
        empty_label=_('No parent category'),
        level_indicator='|--', required=False,
        queryset=proj_models.Category.objects.all())

    def __init__(self, *args, **kwargs):
        super(CategoryAdminForm, self).__init__(*args, **kwargs)
        self.fields['parent'].widget = RelatedFieldWidgetWrapper(
            self.fields['parent'].widget,
            proj_models.Category.parent.field.remote_field,
            self.admin_site)

    def clean_parent(self):
        """ Check if category parent is not selfish. """
        data = self.cleaned_data['parent']
        if data == self.instance:
            raise forms.ValidationError(
                _('A category cannot be parent of itself.'),
                code='self_parenting')
        return data

    class Meta:
        """ CategoryAdminForm's Meta. """
        model = proj_models.Category
        fields = forms.ALL_FIELDS
        widgets = {
            'description': MiniAdminTextarea,
        }


class TaskAdminForm(forms.ModelForm):
    """ Form for Task's Admin. """
    parent = TreeNodeChoiceField(
        label=_('Parent task'),
        empty_label=_('No parent task'),
        level_indicator='|--', required=False,
        queryset=proj_models.Task.objects.all())

    # def __init__(self, *args, **kwargs):
    #     super(TaskAdminForm, self).__init__(*args, **kwargs)
    #     self.fields['parent'].widget = RelatedFieldWidgetWrapper(
    #         self.fields['parent'].widget,
    #         proj_models.Task.parent.field.remote_field,
    #         self.admin_site)

    def clean_parent(self):
        """ Check if task parent is not selfish. """
        data = self.cleaned_data['parent']
        if data == self.instance:
            raise forms.ValidationError(
                _('A task cannot be parent of itself.'),
                code='self_parenting')
        return data

    class Meta:
        """ TaskAdminForm's Meta. """
        model = proj_models.Task
        fields = forms.ALL_FIELDS
        widgets = {
            'description': MiniAdminTextarea,
        }
