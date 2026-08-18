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
    Determine whether a CRM user can create records.
    """

    role = get_user_role(user)

    return role in {
        ROLE_ADMIN,
        ROLE_MANAGER,
        ROLE_SALES,
        ROLE_SUPPORT,
    }


# ==========================================================
# EDIT PERMISSIONS
# ==========================================================

def can_edit(user, obj):
    """
    Determine whether a user can edit a particular CRM object.
    """

    role = get_user_role(user)

    if role in {
        ROLE_ADMIN,
        ROLE_MANAGER,
        ROLE_SUPPORT,
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






