from django import forms
# from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User


# Admin Forms
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
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'])


# # Admin panels
class MyUserAdmin(AuthUserAdmin):
    """ Custom User Admin form """
    fieldsets = (
        (None, {'fields': (('username', 'password'),)}),
        (_('Personal info'), {
            'fields': (
                ('first_name', 'last_name'),
                'email', 'bio', 'photo')}),
        (_('Extra info'), {'fields': (('lang', 'timezone'), )}),
        (_('Permissions'), {'fields': (('is_active', 'is_superuser'), )}),
        (_('Important dates'), {'fields': (('date_joined', 'last_login'), )}),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'full_name')
    list_filter = ('is_superuser', 'is_active')
    search_fields = ('username', 'email', 'full_name')
    ordering = ('username',)
    filter_horizontal = ()
    save_on_top = True
    actions_on_top = True
    actions_on_bottom = True


admin.site.register(User, MyUserAdmin)
