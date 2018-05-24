from django import forms
# from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.utils.translation import ugettext_lazy as _

# from mptt.forms import TreeNodeChoiceField

from ..core.widgets import MiniAdminTextarea


# App forms
class ExpenseForm(forms.Form):
    title = forms.CharField()
    amount = forms.IntegerField()
    category = forms.CharField()


# class TaskAdminForm(forms.ModelForm):
#     """ Form for Task's Admin. """
#     parent = TreeNodeChoiceField(
#         label=_('Parent task'),
#         empty_label=_('No parent task'),
#         level_indicator='|--', required=False,
#         queryset=Task.objects.all())

#     def __init__(self, *args, **kwargs):
#         super(TaskAdminForm, self).__init__(*args, **kwargs)
#         self.fields['parent'].widget = RelatedFieldWidgetWrapper(
#             self.fields['parent'].widget,
#             Task.parent.field.remote_field,
#             self.admin_site)

#     def clean_parent(self):
#         """ Check if task parent is not selfish. """
#         data = self.cleaned_data['parent']
#         if data == self.instance:
#             raise forms.ValidationError(
#                 _('A task cannot be parent of itself.'),
#                 code='self_parenting')
#         return data

#     class Meta:
#         """ TaskAdminForm's Meta. """
#         model = Task
#         fields = forms.ALL_FIELDS
#         widgets = {
#             'description': MiniAdminTextarea,
#         }


# class CategoryAdminForm(forms.ModelForm):
#     """ Form for Category's Admin. """
#     parent = TreeNodeChoiceField(
#         label=_('Parent category'),
#         empty_label=_('No parent category'),
#         level_indicator='|--', required=False,
#         queryset=Category.objects.all())

#     def __init__(self, *args, **kwargs):
#         super(CategoryAdminForm, self).__init__(*args, **kwargs)
#         self.fields['parent'].widget = RelatedFieldWidgetWrapper(
#             self.fields['parent'].widget,
#             Category.parent.field.remote_field,
#             self.admin_site)

#     def clean_parent(self):
#         """ Check if category parent is not selfish. """
#         data = self.cleaned_data['parent']
#         if data == self.instance:
#             raise forms.ValidationError(
#                 _('A category cannot be parent of itself.'),
#                 code='self_parenting')
#         return data

#     class Meta:
#         """
#         CategoryAdminForm's Meta.
#         """
#         model = Category
#         fields = forms.ALL_FIELDS
