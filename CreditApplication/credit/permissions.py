from django.contrib.auth.models import Group, User
from rest_framework import permissions

def is_in_group(user, group_name):
    """
    Takes an user and group name and returns True if the user in that group
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None

class HasGroupPermission(permissions.BasePermission):
    """
    Ensure user is in required group
    """

    def has_permission(self, request, view):
        # Get a mapping of methods -> required group.
        required_groups_mapping = getattr(vies, "required_groups", {})

        # determine the required groups for this particular request method.
        required_groups = required_groups_mapping.get(request.method, [])

        # Return True if user has all the required groups or is staff.
        return all(
            [is_in_group(request.user, group_name) if group_name != "__all__" else True for group_name in required_groups] or
            (request.user and request.user.is_staff)
            )