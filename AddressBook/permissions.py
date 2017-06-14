from rest_framework.permissions import IsAuthenticated


class IsAuthenticatedAndOwnerPermission(IsAuthenticated):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the address book.
        return obj.owner == request.user
