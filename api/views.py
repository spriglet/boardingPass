# api/views.py

from rest_framework import generics
from .serializers import LessonSerializer
from .models import Lesson

class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()