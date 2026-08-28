from crmApp.models import AuditLog


def create_audit_log(
    user,
    action,
    model_name="",
    object_id=None,
    description="",
    request=None,
):
    """
    Create an audit log entry.
    """

    ip_address = None

    if request:
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")

        if forwarded:
            ip_address = forwarded.split(",")[0].strip()
        else:
            ip_address = request.META.get("REMOTE_ADDR")

    return AuditLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=object_id,
        description=description,
        ip_address=ip_address,
    )