# -*- coding: utf-8 -*-
import abc

from functools import reduce
from django.apps import apps

from django.utils.translation import ugettext as _

from . import services


# Base Permission Definition
class ResourcePermission(object):
    """
    Base class for define resource permissions.
    """
    enought_perms = None
    global_perms = None
    retrieve_perms = None
    create_perms = None
    update_perms = None
    destroy_perms = None
    list_perms = None

    def __init__(self, request, view):
        self.request = request
        self.view = view

    def check_permissions(self, action:str, obj:object=None):
        permset = getattr(self, "{}_perms".format(action))

        if isinstance(permset, (list, tuple)):
            permset = reduce(lambda acc, v: acc & v, permset)
        elif permset is None:
            # Use empty operator that always return true with
            # empty components.
            permset = And()
        elif isinstance(permset, PermissionComponent):
            # Do nothing
            pass
        elif inspect.isclass(permset) and issubclass(permset, PermissionComponent):
            permset = permset()
        else:
            raise RuntimeError(_("Invalid permission definition."))

        if self.global_perms:
            permset = (self.global_perms & permset)

        if self.enought_perms:
            permset = (self.enought_perms | permset)

        return permset.check_permissions(request=self.request,
                                         view=self.view,
                                         obj=obj)


class PermissionComponent(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def check_permissions(self, request, view, obj=None):
        pass

    def __invert__(self):
        return Not(self)

    def __and__(self, component):
        return And(self, component)

    def __or__(self, component):
        return Or(self, component)


# Generic Permissions
class AllowAny(PermissionComponent):
    def check_permissions(self, request, view, obj=None):
        return True


class DenyAll(PermissionComponent):
    def check_permissions(self, request, view, obj=None):
        return False


class IsAuthenticated(PermissionComponent):
    def check_permissions(self, request, view, obj=None):
        return request.user and request.user.is_authenticated()


class IsSuperUser(PermissionComponent):
    def check_permissions(self, request, view, obj=None):
        return request.user and request.user.is_authenticated() and request.user.is_superuser


class IsObjectOwner(PermissionComponent):
    def check_permissions(self, request, view, obj=None):
        if obj.owner is None:
            return False

        return obj.owner == request.user


class AllowAnyPermission(ResourcePermission):
    enought_perms = AllowAny()


class IsAuthenticatedPermission(ResourcePermission):
    enought_perms = IsAuthenticated()


class TaigaResourcePermission(ResourcePermission):
    enought_perms = IsSuperUser()


# Project Permissions
class HasProjectPerm(PermissionComponent):
    def __init__(self, perm, *components):
        self.project_perm = perm
        super().__init__(*components)

    def check_permissions(self, request, view, obj=None):
        return services.user_has_perm(request.user, self.project_perm, obj)


class IsProjectAdmin(PermissionComponent):
    def check_permissions(self, request, view, obj=None):
        return services.is_project_admin(request.user, obj)


# Common Permissions
class CommentAndOrUpdatePerm(PermissionComponent):
    def __init__(self, update_perm, comment_perm, *components):
        self.update_perm = update_perm
        self.comment_perm = comment_perm
        super().__init__(*components)

    def check_permissions(self, request, view, obj=None):
        if not obj:
            return False

        project_id = request.DATA.get('project', None)
        if project_id and obj.project_id != project_id:
            project = apps.get_model("projects", "Project").objects.get(pk=project_id)
        else:
            project = obj.project

        data_keys = set(request.DATA.keys()) - {"version"}
        just_a_comment = data_keys == {"comment"}

        if (just_a_comment and services.user_has_perm(request.user, self.comment_perm, project)):
                return True

        return services.user_has_perm(request.user, self.update_perm, project)
