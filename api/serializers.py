# api/serializers.py

from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField


class LessonSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    sensei = serializers.ReadOnlyField(source='owner.username')  # ADD THIS LINE
    seat_cost = serializers.CharField()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Lesson
        fields = ('id', 'sensei','name','description', 'date_created', 'date_modified','seat_cost')
        read_only_fields = ('date_created', 'date_modified','cost_amount_currency')


class TimeSlotStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeSlotStatus
        read_only_fields = ('id','name')


class TimeSlotSerializer(serializers.ModelSerializer):
    """Serializer to map the TimeSlot model to a JSON format"""

    class Meta:
        """Mapts the this serializer to the TimeSlot model"""
        model = TimeSlot
        fields = ('id', 'lesson', 'start','status')


class SeatSerializer(serializers.ModelSerializer):
    """Serializer to convert the Seat model to a json format"""
    cost = serializers.CharField()

    class Meta:
        model = Seat
        fields = ('student', 'status', 'time_slot', 'cost')


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer to convert Transaction Model"""
    amount = serializers.CharField()

    class Meta:
        model = Transaction
        fields = ('status', 'seat','amount')


class UserSerializer(serializers.ModelSerializer):
    """A user serializer to aid in authentication and authorization."""

    class Meta:
        """Map this serializer to the default django user model."""
        model = User
        fields = ('id', 'username', 'first_name','last_name')


class SenseiSerializer(serializers.ModelSerializer):
    """A serializer that displays Sensei info"""
    user = UserSerializer(required=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'country')