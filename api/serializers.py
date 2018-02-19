# api/serializers.py

from rest_framework import serializers
from .models import Lesson
from django.contrib.auth.models import User

class LessonSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    sensei = serializers.ReadOnlyField(source='owner.username')  # ADD THIS LINE
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Lesson
        fields = ('id', 'sensei','name','description', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')

class UserSerializer(serializers.ModelSerializer):
    """A user serializer to aid in authentication and authorization."""

    lesson = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Lesson.objects.all())

    class Meta:
        """Map this serializer to the default django user model."""
        model = User
        fields = ('id', 'username', 'lessons')