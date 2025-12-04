from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


ADMIN_GROUP_NAME = "administrador"
MANAGER_GROUP_NAME = "gestor"


def bootstrap_portal_data(stdout=None, style=None):
    """Create default groups and seed initial users.

    This helper is shared by multiple management commands to keep the
    provisioning logic in one place and idempotent.
    """

    user_model = get_user_model()
    user_ct = ContentType.objects.get_for_model(user_model)

    admin_group, _ = Group.objects.get_or_create(name=ADMIN_GROUP_NAME)
    manager_group, _ = Group.objects.get_or_create(name=MANAGER_GROUP_NAME)

    perms = Permission.objects.filter(
        content_type=user_ct,
        codename__in=[
            "add_user",
            "change_user",
            "delete_user",
            "view_user",
        ],
    )
    admin_group.permissions.set(perms)

    manager_perms = perms.exclude(codename="delete_user")
    manager_group.permissions.set(manager_perms)

    admin_user, _ = user_model.objects.get_or_create(
        username="jrodas",
        defaults={"email": "jrodas@example.com"},
    )
    admin_user.first_name = admin_user.first_name or "Julio"
    admin_user.last_name = admin_user.last_name or "Rodas"
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.set_password("99998888")
    admin_user.save()
    admin_user.groups.add(admin_group)

    manager_user, _ = user_model.objects.get_or_create(
        username="rodas",
        defaults={"email": "rodas@example.com"},
    )
    manager_user.first_name = manager_user.first_name or "Rodas"
    manager_user.last_name = manager_user.last_name or "Gestor"
    manager_user.is_staff = True
    manager_user.is_superuser = False
    manager_user.set_password("99998888")
    manager_user.save()
    manager_user.groups.add(manager_group)

    if stdout and style:
        stdout.write(style.SUCCESS("Grupos y usuarios iniciales configurados."))
