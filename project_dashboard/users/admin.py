from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.flatpages.admin import FlatPageAdmin as BaseFlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _

from .models import User


# Customize Admin Site
admin.sites.AdminSite.site_header = 'project_dashboard Administration'
admin.sites.AdminSite.site_title = 'project_dashboard Administration'


# Register models
class MyUserChangeForm(UserChangeForm):
    """ User change form for Admin """
    class Meta(UserChangeForm.Meta):
        """ Meta for User change form """
        model = User


class MyUserCreationForm(UserCreationForm):
    """ User create form for Admin """
    error_message = UserCreationForm.error_messages.update({
        'duplicate_username': 'This username has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        """ Meta for User create form """
        model = User

    def clean_username(self):
        """ Clean username """
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


@admin.register(User)
class MyUserAdmin(AuthUserAdmin):
    """ Custom User Admin form """
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = (
        ('User Profile', {'fields': ('name',)}),
    ) + AuthUserAdmin.fieldsets
    list_display = ('username', 'name', 'is_superuser')
    search_fields = ['name']


class FlatPageAdmin(BaseFlatPageAdmin):
    """ Define a new FlatPageAdmin  """
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse', ),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
