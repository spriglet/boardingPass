from rest_framework.permissions import BasePermission
from .models import Lesson



class IsOwner(BasePermission):
    """Custom permission class to allow only lesson owners to edit them."""

    def has_obj_permission(self, request, view, obj):
        """Return True if permission is granted to the bucketlist owner."""
        print(request.user.id+"= SENSEI:"+obj.sensei.id)
        if isinstance(obj, Lesson):
            return obj.sensei == request.user
        return obj.sensei == request.user

