from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# from django.contrib.flatpages import views as flat_views
from django.urls import path, include
from django.views.generic import TemplateView
from django.views import defaults as default_views


urlpatterns = [
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('pages/', include('django.contrib.flatpages.urls')),
    # Example flatpage path
    # path('tos/', flat_views.flatpage, {'url': 'tos/'}, name='tos'),

    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_DOCS_URL, include('django.contrib.admindocs.urls')),
    path(settings.ADMIN_URL, admin.site.urls),

    # Third party URLs
    path('accounts/', include('allauth.urls')),
    path('crud/', include('crudbuilder.urls')),

    # Custom apps
    # path('projects/', include('project_dashboard.projects.urls', namespace='project')),
    path('users/', include('project_dashboard.users.urls', namespace='users')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path('400/', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        path('403/', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        path('404/', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        path('500/', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
