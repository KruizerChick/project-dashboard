from django import forms

from .models import Project, Category, Expense


# App forms
class ExpenseForm(forms.Form):
    title = forms.CharField()
    amount = forms.IntegerField()
    category = forms.CharField()
