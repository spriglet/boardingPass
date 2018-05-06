# api/views.py

from rest_framework import generics
from .serializers import LessonSerializer,SenseiSerializer, UserSerializer,TimeSlotSerializer,SeatSerializer,TransactionSerializer
from .permissions import IsOwner
from .models import *
from rest_framework import permissions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


class CreateLessonView(generics.ListCreateAPIView):

    """This class defines the create behavior of our rest api."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a lesson."""
        serializer.save(sensei=self.request.user)  # Add owner=self.request.user


class CreateTimeSlotView(generics.ListCreateAPIView):
    #permission_classes = (permissions.IsAuthenticated,IsOwner)  # ADD THIS LINE

    """This class defines the create behavior of our rest api."""
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    # permission_classes = (permissions.IsAuthenticated,IsLessonOwner)  # ADD THIS LINE




class SeatView(generics.ListCreateAPIView):
    """Creates a seat in the lesson/class"""
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    def perform_create(self, serializer):
        """Save the post data when creating a lesson."""
        serializer.save(student=self.request.user)  # Add owner=self.request.user


class CreateTransaction(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = TransactionSerializer


class LessonView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner)


class SenseiLessonView(generics.ListAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    serializer_class = LessonSerializer
    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """

        sensei = self.kwargs['sensei']
        return Lesson.objects.filter(sensei=sensei)

class MyLessonsView(generics.ListAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    serializer_class = LessonSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """

        return Lesson.objects.filter(sensei=self.request.user)


class TimeSlotView(generics.RetrieveUpdateDestroyAPIView):
    """This calass handles the http GET,PUT and DELETE request for timeslots"""
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer


class TransactionView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles GET,PUT and DELETE request for transactions"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class UserView(generics.ListAPIView):
    """View to list the user queryset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLessonView(generics.RetrieveAPIView):
    """View to retrieve a user instance."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SenseiView(generics.ListAPIView):
    """View to see the avilable teachers"""
    queryset = UserProfile.objects.filter(isSensei=True)
    serializer_class = SenseiSerializer


class SenseiViewProfileData(generics.ListAPIView):
    """View to see the avilable teachers"""
    serializer_class = SenseiSerializer
    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """

        user = self.kwargs['user']
        return UserProfile.objects.filter(user=user)