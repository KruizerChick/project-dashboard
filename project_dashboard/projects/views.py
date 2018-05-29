from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.generic import CreateView
# from django.views.generic.list import ListView

import json

from .forms import ExpenseForm
from . import models as proj_models


# Create your views here.
def project_list(request):
    project_list = proj_models.Project.objects.all()
    return render(
        request, 'projects/project-list.html',
        {'project_list': project_list}
        )


def open_projects(request):
    project_list = proj_models.Project.open_projects.all()
    return render(
        request, 'projects/project-list.html',
        # request, 'pages/home.html',
        {'project_list': project_list}
        )


def project_detail(request, project_slug):
    # fetch the correct project
    project = get_object_or_404(proj_models.Project, slug=project_slug)

    if request.method == 'GET':
        category_list = proj_models.Category.objects.filter(project=project)
        return render(
            request, 'projects/project-detail.html',
            {'project': project,
             'expense_list': project.expenses.all(),
             'category_list': category_list, })

    elif request.method == 'POST':
        # Process the form
        form = ExpenseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category']

            category = get_object_or_404(
                proj_models.Category, project=project, name=category_name)

            proj_models.Expense.objects.create(
                project=project,
                title=title,
                amount=amount,
                category=category
            ).save()

    elif request.method == 'DELETE':
        # Delete categories
        id = json.loads(request.body)['id']
        expense = get_object_or_404(proj_models.Expense, id=id)
        expense.delete()
        return HttpResponse('')

    return HttpResponseRedirect(project_slug)


class ProjectCreateView(CreateView):
    model = proj_models.Project
    template_name = 'projects/add-project.html'
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        categories = self.request.POST['categoriesString'].split(',')
        for category in categories:
            proj_models.Category.objects.create(
                project=proj_models.Project.objects.get(id=self.object.id),
                name=category
            ).save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return slugify(self.request.POST['name'])


# class ProjectListView(ListView):
#     model = proj_models.Project

#     def get_queryset(self):
#         queryset = super(ProjectListView, self).get_queryset()
#         queryset = proj_models.Project.open_projects.all()
#         return queryset
