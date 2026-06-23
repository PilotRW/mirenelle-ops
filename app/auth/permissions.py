from collections.abc import Iterable

PERMISSIONS = {
    "ops:view",
    "ops:operate",
    "ops:finance",
    "ops:configure",
    "ops:admin",
}

ROLE_PERMISSIONS = {
    "owner": PERMISSIONS,
    "ops_manager": {
        "ops:view",
        "ops:operate",
        "ops:finance",
        "ops:configure",
    },
    "ops_operator": {
        "ops:view",
        "ops:operate",
    },
    "ops_finance": {
        "ops:view",
        "ops:finance",
    },
    "ops_viewer": {
        "ops:view",
    },
}


def normalize_roles(values: Iterable[str]) -> list[str]:
    roles: list[str] = []
    for value in values:
        role = value.strip()
        if not role:
            continue
        role = role.rsplit("/", 1)[-1].rsplit(":", 1)[-1]
        if role in ROLE_PERMISSIONS and role not in roles:
            roles.append(role)
    return roles


def permissions_for_roles(roles: Iterable[str]) -> list[str]:
    permissions: set[str] = set()
    for role in roles:
        permissions.update(ROLE_PERMISSIONS.get(role, set()))
    return sorted(permissions)


def has_permission(permissions: Iterable[str], permission: str) -> bool:
    permission_set = set(permissions)
    return "ops:admin" in permission_set or permission in permission_set
