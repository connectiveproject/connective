from rest_framework.permissions import SAFE_METHODS, BasePermission


class AllowCoordinator(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.user_type == request.user.Types.COORDINATOR


class AllowSupervisor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.user_type == request.user.Types.SUPERVISOR


class AllowConsumer(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.user_type == request.user.Types.CONSUMER


class AllowInstructor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.user_type == request.user.Types.INSTRUCTOR


class AllowVendor(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.user_type == request.user.Types.VENDOR


class AllowCoordinatorReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return (
            request.method in SAFE_METHODS
            and request.user.user_type == request.user.Types.COORDINATOR
        )


class AllowConsumerReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return (
            request.method in SAFE_METHODS
            and request.user.user_type == request.user.Types.CONSUMER
        )


class AllowInstructorReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return (
            request.method in SAFE_METHODS
            and request.user.user_type == request.user.Types.INSTRUCTOR
        )


class AllowVendorReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return (
            request.method in SAFE_METHODS
            and request.user.user_type == request.user.Types.VENDOR
        )
