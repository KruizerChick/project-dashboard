from django import forms

# from . import models


# App forms
class ExpenseForm(forms.Form):
    title = forms.CharField()
    amount = forms.IntegerField()
    category = forms.CharField()


# Crud Forms
# class CrudProjectForm(forms.ModelForm):
#     """ Form to handle Entry posts """

#     class Meta:
#         model = models.Project
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         # self.request = kwargs.pop('request', None)
#         super(CrudProjectForm, self).__init__(*args, **kwargs)
