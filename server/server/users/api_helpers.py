import logging
from functools import partial
from typing import Dict, Iterable, List, Set

from rest_framework.permissions import SAFE_METHODS, BasePermission

from server.users.models import RoleScope, UserRole
from server.utils.permission_classes import AllowAuthenticatedReadOnly
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

    privileges_read = []
    privileges_read_school = []
    privileges_read_organization = []

    privileges_write = []
    privileges_write_school = []
    privileges_write_organization = []

    def is_safe_method(self, request) -> bool:
        return request.method in SAFE_METHODS

    def _get_needed_privileges(self, request, school: bool, organization: bool) -> Set:
        result: Set = set(self.privileges_write)
        if school:
            result.update(self.privileges_write_school)
        if organization:
            result.update(self.privileges_write_organization)
        if self.is_safe_method(request):
            result.update(self.privileges_read)
            if school:
                result.update(self.privileges_read_school)
            if organization:
                result.update(self.privileges_read_organization)
        return result

    def get_allowed_schools(self, request) -> Set:
        user = request.user
        result: Set = set()
        scopes: Dict[str, RoleScope] = user.get_privilege_scopes()
        needed_privileges = self._get_needed_privileges(request, True, False)
        for privilege in needed_privileges:
            if privilege in scopes:
                result.update(scopes[privilege].get_schools())
        return result

    def get_allowed_organizations(self, request) -> Set:
        user = request.user
        result: Set = set()
        scopes: Dict[str, RoleScope] = user.get_privilege_scopes()
        needed_privileges = self._get_needed_privileges(request, False, True)
        for privilege in needed_privileges:
            if privilege in scopes:
                result.update(scopes[privilege].get_organizations())
        return result

    def is_admin_scope(self, request) -> bool:
        user = request.user
        scopes: Dict[str, RoleScope] = user.get_privilege_scopes()
        needed_privileges = self._get_needed_privileges(request, True, True)
        for privilege in needed_privileges:
            if privilege in scopes and scopes[privilege].is_admin_scope():
                return True
        return False


class HasPrivilege(BasePermission):
    def __init__(self, privileges):
        self.privileges = privileges

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return has_any_privilege(self.privileges, request.user)


def privilege_class(privileges: Iterable) -> HasPrivilege:
    return partial(HasPrivilege, privileges)


def has_any_privilege(privileges, user) -> bool:
    return bool(get_relevant_roles(privileges, user))


def get_privilege_permission_classes(
    privileges_read, privileges_write
) -> List[BasePermission]:
    return (
        privilege_class(privileges_read) & AllowAuthenticatedReadOnly
    ) | privilege_class(privileges_write)
