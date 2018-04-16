from django.db import models

# Create your models here.
# /api/models.py
from djmoney.models.fields import MoneyField
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver


class Lesson(models.Model):
    """This class represents the bucketlist model."""
    name = models.CharField(max_length=255, blank=False, unique=False)
    description = models.CharField(max_length=255,blank=False,unique=False)
    sensei = models.ForeignKey('auth.User',  # ADD THIS FIELD
                        related_name='sensei',
                        on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    student_threshold = models.PositiveIntegerField(default=1) # the maximum students in the lesson
    length_in_minutes = models.PositiveIntegerField(blank=False,default=30) # length of the lesson in minutes
    seat_cost = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='JPY',
        max_digits=13,
    )

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)


class TimeSlotStatus(models.Model):
    """Status for the time slot. Cancelled,Completed,Scheduled"""
    name = models.CharField(max_length=31)
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)


class TimeSlot(models.Model):
    """The time slots for the lesson"""
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name='lesson')
    start = models.DateTimeField(blank=False)
    status = models.ForeignKey(TimeSlotStatus,on_delete=models.CASCADE,default=1,related_name='status')
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.lesson)

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True,on_delete=models.CASCADE)
    company = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50,blank=False,default='USA')
    currency = models.CharField(max_length=31,blank=False,default='JPY')
    isSensei = models.BooleanField(default=False)
    timeZone = models.CharField(max_length=31,default='UTC')


class SeatStatus(models.Model):
    name = models.CharField(max_length=31,blank=False)
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)

class Seat(models.Model):
    student = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    status = models.ForeignKey(SeatStatus,on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot,on_delete=models.CASCADE)
    cost = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='JPY',
        max_digits=13,
    )


class TransactionStatus(models.Model):
    """Different transaction status"""
    name = models.CharField(max_length=31)
    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)

class Transaction(models.Model):
    """Transaction associated with seats that students buy"""
    status = models.ForeignKey(TransactionStatus, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    amount = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='JPY',
        max_digits=13,
    )


# This receiver handles token creation immediately a new user is created.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)