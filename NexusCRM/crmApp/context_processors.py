from .permissions import (
    get_user_role,
    can_create,
    ROLE_ADMIN,
    ROLE_MANAGER,
    ROLE_SUPPORT,
)


def crm_permissions(request):
    """
    Make common CRM permissions available to all templates.
    """

    user = request.user

    if not user.is_authenticated:
        return {
            "crm_role": None,
            "can_create_records": False,
            "can_edit_all_records": False,
            "can_delete_records": False,
        }

    role = get_user_role(user)

    return {
        "crm_role": role,

        "can_create_records": can_create(user),

        "can_edit_all_records": role in {
            ROLE_ADMIN,
            ROLE_MANAGER,
            ROLE_SUPPORT,
        },

        "can_delete_records": role in {
            ROLE_ADMIN,
            ROLE_MANAGER,
        },
    }



