from rest_framework.permissions import SAFE_METHODS, BasePermission


class AllowCoordinator(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == request.user.Types.COORDINATOR


class AllowConsumer(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == request.user.Types.CONSUMER


class AllowVendor(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == request.user.Types.VENDOR


class AllowCoordinatorReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            and request.user.user_type == request.user.Types.COORDINATOR
        )


class AllowConsumerReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            and request.user.user_type == request.user.Types.CONSUMER
        )
