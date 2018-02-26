# api/views.py

from rest_framework import generics
from .serializers import LessonSerializer,UserSerializer,TimeSlotSerializer,SeatSerializer
from .permissions import IsLessonOwner
from .models import *
from rest_framework import permissions
from django.contrib.auth.models import User

class CreateLessonView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (permissions.IsAuthenticated,IsLessonOwner)  # ADD THIS LINE

    def perform_create(self, serializer):
        """Save the post data when creating a lesson."""
        serializer.save(sensei=self.request.user)  # Add owner=self.request.user

class CreateTimeSlotView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    # permission_classes = (permissions.IsAuthenticated,IsLessonOwner)  # ADD THIS LINE

class CreateSeatView(generics.ListCreateAPIView):
    """Creates a seat in the lesson/class"""
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class LessonView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsLessonOwner)
class TimeSlotView(generics.RetrieveAPIView):
    """This calass handles the http GET,PUT and DELETE request for timeslots"""
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer


class UserView(generics.ListAPIView):
    """View to list the user queryset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLessonView(generics.RetrieveAPIView):
    """View to retrieve a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer