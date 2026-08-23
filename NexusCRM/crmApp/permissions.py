from functools import wraps

from django.core.exceptions import PermissionDenied


# ==========================================================
# ROLE CONSTANTS
# ==========================================================

ROLE_ADMIN = "admin"
ROLE_MANAGER = "manager"
ROLE_SALES = "sales"
ROLE_SUPPORT = "support"
ROLE_VIEWER = "viewer"


# ==========================================================
# USER ROLE HELPERS
# ==========================================================

def get_user_role(user):
    """
    Return the CRM role assigned to the user.

    Superusers are always treated as administrators.
    Users without a Profile are treated as viewers.
    """

    if not user or not user.is_authenticated:
        return None

    if user.is_superuser:
        return ROLE_ADMIN

    profile = getattr(user, "profile", None)

    if not profile:
        return ROLE_VIEWER

    return profile.role


def is_admin(user):
    return get_user_role(user) == ROLE_ADMIN


def is_manager(user):
    return get_user_role(user) == ROLE_MANAGER


def is_sales(user):
    return get_user_role(user) == ROLE_SALES


def is_support(user):
    return get_user_role(user) == ROLE_SUPPORT


def is_viewer(user):
    return get_user_role(user) == ROLE_VIEWER


# ==========================================================
# CREATE PERMISSIONS
# ==========================================================

def can_create(user):
    """
    Determine whether a CRM user can create CRM records.

    Admin, Manager and Sales can create records.
    Support and Viewer are read-only.
    """

    role = get_user_role(user)

    return role in {
        ROLE_ADMIN,
        ROLE_MANAGER,
        ROLE_SALES,
    }


# ==========================================================
# EDIT PERMISSIONS
# ==========================================================

def can_edit(user, obj):
    """
    Determine whether a user can edit a particular CRM object.

    Admin and Manager:
        Can edit any record.

    Sales:
        Can edit records they own.

    Support and Viewer:
        Read-only.
    """

    role = get_user_role(user)

    if role in {
        ROLE_ADMIN,
        ROLE_MANAGER,
    }:
        return True

    if role == ROLE_SALES:
        return obj.owner_id == user.id

    return False


# ==========================================================
# DELETE PERMISSIONS
# ==========================================================

def can_delete(user, obj):
    """
    Determine whether a user can delete a particular CRM object.

    Only Admin and Manager can delete records.
    """

    role = get_user_role(user)

    return role in {
        ROLE_ADMIN,
        ROLE_MANAGER,
    }

# ==========================================================
# DEAL PERMISSIONS
# ==========================================================

def can_manage_deals(user):
    """
    Determine whether a user can manage deals.

    Admin and Manager can manage all deals.
    Sales can manage deals they own.
    Support and Viewer are read-only.
    """

    role = get_user_role(user)

    return role in {
        ROLE_ADMIN,
        ROLE_MANAGER,
        ROLE_SALES,
    }


def can_edit_deal(user, deal):
    """
    Determine whether a user can edit a particular deal.

    Admin and Manager:
        Can edit any deal.

    Sales:
        Can edit deals they own.

    Support and Viewer:
        Read-only.
    """

    return can_edit(user, deal)


def can_delete_deal(user, deal):
    """
    Determine whether a user can delete a particular deal.

    Only Admin and Manager can delete deals.
    """

    return can_delete(user, deal)


def can_change_deal_stage(user, deal):
    """
    Determine whether a user can change the stage of a deal.

    Admin and Manager:
        Any deal.

    Sales:
        Their own deals.

    Support and Viewer:
        Cannot change stages.
    """

    return can_edit_deal(user, deal)


def can_manage_pipelines(user):
    """
    Determine whether a user can create, edit, or delete
    pipelines and pipeline stages.

    Only Admin and Manager can manage pipeline configuration.
    """

    role = get_user_role(user)

    return role in {
        ROLE_ADMIN,
        ROLE_MANAGER,
    }

# ==========================================================
# ACTIVITY PERMISSIONS
# ==========================================================

def can_manage_activities(user):
    """
    Determine whether a user can create activities.

    Admin, Manager and Sales can create activities.
    Support and Viewer are read-only.
    """

    role = get_user_role(user)

    return role in {
        ROLE_ADMIN,
        ROLE_MANAGER,
        ROLE_SALES,
    }


def can_view_activity(user, activity):
    """
    Determine whether a user can view an activity.

    Admin, Manager, Sales, Support and Viewer
    can view activities.

    Authentication is handled by the calling view.
    """

    role = get_user_role(user)

    return role in {
        ROLE_ADMIN,
        ROLE_MANAGER,
        ROLE_SALES,
        ROLE_SUPPORT,
        ROLE_VIEWER,
    }


def can_edit_activity(user, activity):
    """
    Determine whether a user can edit an activity.

    Admin and Manager:
        Can edit any activity.

    Sales:
        Can edit activities they created or are assigned to.

    Support and Viewer:
        Read-only.
    """

    role = get_user_role(user)

    if role in {
        ROLE_ADMIN,
        ROLE_MANAGER,
    }:
        return True

    if role == ROLE_SALES:
        return (
            activity.created_by_id == user.id
            or activity.assigned_to_id == user.id
        )

    return False


def can_delete_activity(user, activity):
    """
    Determine whether a user can delete an activity.

    Only Admin and Manager can delete activities.
    """

    role = get_user_role(user)

    return role in {
        ROLE_ADMIN,
        ROLE_MANAGER,
    }

# def can_manage_activities(user):
#     """
#     Determine whether a user can create activities.

#     Admin, Manager and Sales can create activities.
#     Support and Viewer are read-only.
#     """

#     role = get_user_role(user)

#     return role in {
#         ROLE_ADMIN,
#         ROLE_MANAGER,
#         ROLE_SALES,
#     }


def can_edit_activity(user, activity):
    """
    Determine whether a user can edit a particular activity.

    Admin and Manager:
        Can edit any activity.

    Sales:
        Can edit activities they created or are assigned to.

    Support and Viewer:
        Read-only.
    """

    role = get_user_role(user)

    if role in {
        ROLE_ADMIN,
        ROLE_MANAGER,
    }:
        return True

    if role == ROLE_SALES:
        return (
            activity.created_by_id == user.id
            or activity.assigned_to_id == user.id
        )

    return False


def can_delete_activity(user, activity):
    """
    Determine whether a user can delete a particular activity.

    Only Admin and Manager can delete activities.
    """

    role = get_user_role(user)

    return role in {
        ROLE_ADMIN,
        ROLE_MANAGER,
    }



# ==========================================================
# DECORATORS
# ==========================================================

def crm_permission(check_function):
    """
    Generic permission decorator for CRM actions.
    """

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                raise PermissionDenied

            if not check_function(request.user):
                raise PermissionDenied

            return view_func(
                request,
                *args,
                **kwargs
            )

        return wrapper

    return decorator


def crm_can_create(view_func):
    """
    Restrict a view to users who can create CRM records.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not can_create(request.user):
            raise PermissionDenied

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper






