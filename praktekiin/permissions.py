from rest_framework import permissions

class CustomModelPermissions(permissions.DjangoModelPermissions):
    """
    Permission for any request methods.
    """
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        has_perm = super().has_permission(request, view)

        queryset = self._queryset(view)
        perms = self.get_required_permissions(request.method, queryset.model)
        change_perm = self.get_required_permissions('PUT', queryset.model)

        user = request.user
        if request.method == 'GET':
            has_perm = has_perm \
                or user.has_perms(perms) \
                or user.has_perms(change_perm)
        return has_perm
