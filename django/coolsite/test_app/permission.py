from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
    

class IsAdminOrOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS: GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(
            request.user and request.user.is_authenticated and (
                request.user.is_staff or obj.author == request.user
            )
        )
