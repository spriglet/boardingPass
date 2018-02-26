# api/serializers.py

from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField

class LessonSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    sensei = serializers.ReadOnlyField(source='owner.username')  # ADD THIS LINE
    time_slot = serializers.StringRelatedField(many=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Lesson
        fields = ('id', 'sensei','name','description', 'date_created', 'date_modified','seat_cost','time_slot')
        read_only_fields = ('date_created', 'date_modified')
class TimeSlotSerializer(serializers.ModelSerializer):
    """Serializer to map the TimeSlot model to a JSON format"""

    seat = serializers.StringRelatedField(many=True)
    class Meta:
        """Mapts the this serializer to the TimeSlot model"""
        model = TimeSlot
        fields = ('id','lesson','start','seat')
class SeatSerializer(serializers.ModelSerializer):
    """Serializer to convert the Seat model to a json format"""
    cost = MoneyField(max_digits=10, decimal_places=2)
    class Meta:
        model = Seat
        fields = ('student','status','time_slot','cost')


class UserSerializer(serializers.ModelSerializer):
    """A user serializer to aid in authentication and authorization."""

    lesson = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Lesson.objects.all())

    class Meta:
        """Map this serializer to the default django user model."""
        model = User
        fields = ('id', 'username', 'lessons')