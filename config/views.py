""" Views for the Project Dashboard Website """

from django.views.generic import TemplateView

from project_dashboard.projects.models import Project


class DashboardView(TemplateView):
    template_name = 'pages/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context.update({
            'projects': Project.open_projects.all(),
            'issues': '',
            'tasks': '',
            }
        )
        return context
