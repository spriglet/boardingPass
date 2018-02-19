# api/views.py

from rest_framework import generics
from .serializers import LessonSerializer,UserSerializer
from .permissions import IsOwner
from .models import Lesson
from rest_framework import permissions
from django.contrib.auth.models import User

class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwner)  # ADD THIS LINE

    def perform_create(self, serializer):
        """Save the post data when creating a lesson."""
        serializer.save(sensei=self.request.user)  # Add owner=self.request.user

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner)

class UserView(generics.ListAPIView):
    """View to list the user queryset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailsView(generics.RetrieveAPIView):
    """View to retrieve a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer