""" Services used for the project model """
# from django.db.models import Q

# from .models.project import Membership


# def get_visible_project_ids(from_stakeholder, by_stakeholder):
#     """Calculate the project_ids from one stakeholder visible by another"""
#     required_permissions = ["view_project"]
#     # Or condition for membership filtering, the basic one is the access to projects
#     # allowing anonymous visualization
#     member_perm_conditions = Q(project__anon_permissions__contains=required_permissions)

#     # Authenticated
#     if by_stakeholder.is_authenticated():
#         # Calculating the projects wich from_stakeholder stakeholder is member
#         by_stakeholder_project_ids = by_stakeholder.memberships.values_list("project__id", flat=True)
#         # Adding to the condition two OR situations:
#         # - The from stakeholder has a role that allows access to the project
#         # - The to stakeholder is the owner
#         member_perm_conditions |= \
#             Q(project__id__in=by_stakeholder_project_ids, role__permissions__contains=required_permissions) |\
#             Q(project__id__in=by_stakeholder_project_ids, is_admin=True)

#     # Calculating the stakeholder memberships adding the permission filter for the by stakeholder
#     memberships_qs = Membership.objects.filter(member_perm_conditions, stakeholder=from_stakeholder)
#     project_ids = memberships_qs.values_list("project__id", flat=True)
#     return project_ids
