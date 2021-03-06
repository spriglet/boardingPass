from rest_framework.permissions import BasePermission
from .models import Lesson

class IsLessonOwner(BasePermission):
    """Custom permission class to allow only bucketlist owners to edit them."""

    def has_obj_permission(self, request, view, obj):
        """Return True if permission is granted to the bucketlist owner."""
        if isinstance(obj, Lesson):
            return obj.sensei == request.user
        return obj.sensei == request.user

