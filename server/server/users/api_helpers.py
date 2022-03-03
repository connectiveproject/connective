import logging
from typing import Dict, List, Set

from rest_framework.permissions import BasePermission

from server.users.models import RoleScope, UserRole
from server.utils.privileges import ROLES

logger = logging.getLogger(__name__)


def get_relevant_roles(required_privileges, user) -> List[UserRole]:
    result: List[UserRole] = []
    roles: UserRole = user.roles.all()
    user_role: UserRole
    for user_role in roles:
        if user_role.role_code not in ROLES:
            logger.warning(f"Unknown role: {user_role.role_code}")
            continue
        user_privileges = ROLES[user_role.role_code]
        if any(
            required_priv in user_privileges for required_priv in required_privileges
        ):
            result.append(user_role)
    return result


class PrivilegeAccessMixin:

    privileges = []

    def get_allowed_schools(self, user) -> List:
        result: Set = set()
        scopes: Dict[str, RoleScope] = user.get_privilege_scopes()
        for privilege in self.privileges:
            if privilege in scopes:
                result.add(scopes[privilege].get_schools())
        return result

    def get_allowed_organizations(self, user):
        result: Set = set()
        scopes: Dict[str, RoleScope] = user.get_privilege_scopes()
        for privilege in self.privileges:
            if privilege in scopes:
                result.add(scopes[privilege].get_organizations())
        return result

    def is_admin_scope(self, user):
        scopes: Dict[str, RoleScope] = user.get_privilege_scopes()
        for privilege in self.privileges:
            if privilege in scopes and scopes[privilege].is_admin_scope():
                return True
        return False


class HasPrivilege(BasePermission):
    def __init__(self, privileges):
        self.privileges = privileges

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return bool(get_relevant_roles(self.privileges, request.user))
