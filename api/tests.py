# api test.py

from django.test import TestCase
from .models import *
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status




# Create your tests here.
class ModelTestCase(TestCase):
    def setUp(self):
        """Define the for Lesson and other variables"""
        self.sensei = User.objects.create(username="Sensei")  # ADD THIS LINE
        self.student = User.objects.create(username="Student")
        self.name = "My Cool Class"
        self.description = "This is a class for only, if you think you are cool then apply."
        self.userProfile = UserProfile(user=self.sensei, company='Test Company',currency='US', country='USA', isSensei=True,timeZone="UTC")

        self.time_slot_status = TimeSlotStatus(name='Scheduled')
        self.time_slot_status.save()
        self.transaction_status = TransactionStatus(name="accepted")
        self.studentProfile = UserProfile(user=self.student,country='Japan')

        self.seat_status = SeatStatus(name="TEST")

        self.seat_status.save()

    def test_model_can_create_profile(self):
        """Test create user profile"""
        old_count = UserProfile.objects.count()
        self.userProfile.save()
        new_count = UserProfile.objects.count()
        self.assertNotEqual(new_count,old_count)
    def test_model_can_create_lesson(self):
        """Test the lesson model can create a lesson."""
        self.lesson = Lesson(name=self.name, description=self.description, sensei=self.sensei, length_in_minutes=30,seat_cost=14.40)
        old_count = Lesson.objects.count()
        self.lesson.save()
        new_count = Lesson.objects.count()
        self.assertNotEqual(old_count, new_count)
    def test_model_can_create_time_slot(self):
        """Test to make can creat time slot record"""
        lesson = Lesson(name=self.name, description=self.description, sensei=self.sensei, length_in_minutes=30,seat_cost=5.00)
        old_count = Lesson.objects.count()
        lesson.save()
        time_slot = TimeSlot(start="2018-03-02 10:00",lesson=lesson,status=self.time_slot_status)
        old_count = TimeSlot.objects.count()
        time_slot.save()
        new_count = TimeSlot.objects.count()
        self.assertNotEqual(old_count,new_count)

    def test_model_can_create_student_profile(self):
        """Creates student profile"""
        old_count = UserProfile.objects.count()
        self.studentProfile.save()
        new_count = UserProfile.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_seat(self):
        """Test to make can creat time slot record"""
        lesson = Lesson(name=self.name, description=self.description, sensei=self.sensei, length_in_minutes=30,seat_cost=12.00)
        old_count = Lesson.objects.count()
        lesson.save()
        time_slot = TimeSlot(start="2018-03-02 10:00", lesson=lesson, status=self.time_slot_status)
        old_count = TimeSlot.objects.count()
        time_slot.save()
        self.seat = Seat(cost=lesson.seat_cost, status=self.seat_status, student=self.student, time_slot=time_slot)
        old_count = Seat.objects.count()
        self.seat.save()
        new_count = Seat.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_transaction_status(self):
        old_count = TransactionStatus.objects.count()
        self.transaction_status.save()
        new_count = TransactionStatus.objects.count()
        self.assertNotEqual(old_count, new_count)
# Define this after the ModelTestCase
class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create(username="nerd")

        # Initialize client and force it to use authentication
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.lesson_data = {'name': 'Japanese Class' , 'description':'Join to learn Japanese','sensei': user.id,'seat_cost':'10.94'}
        self.response = self.client.post(reverse('create'), self.lesson_data,format="json")
        self.time_slot_status = TimeSlotStatus(name='Scheduled')
        self.time_slot_status.save()
        self.transaction_status = TransactionStatus(name="accepted")


        self.seat_status = SeatStatus(name="TEST")

        self.seat_status.save()
    def test_api_can_create_a_lesson(self):
        """Test the api has lesson creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
    def test_api_can_create_time_slot(self):
        """Test to makes sure user can create time slot"""
        user = User.objects.create(username="Tom")
        lesson = Lesson(name='Test Lesson', description='Test', sensei=user, length_in_minutes=30,status=self.time_slot_status)
        lesson.save()
        time_slot = {'lesson':lesson.id,'start':'2018-03-02 10:00'}
        self.response = self.client.post(reverse('create'),time_slot,format="json")

    def test_api_can_create_seat(self):
        """Test to makes sure user can create time slot"""
        user = User.objects.create(username="Some Student")
        lesson = Lesson(name='Test Lesson', description='Test', sensei=user, length_in_minutes=30,status=self.seat_status)
        lesson.save()
        time_slot = TimeSlot(lesson=lesson,start='2018-03-02 14:00',status=1)
        time_slot.save();
        seat_status = SeatStatus(name="TEST")
        seat_status.save()
        seat_data = {'student':user.id,'status':seat_status.id}

        self.response = self.client.post(reverse('create'), seat_data, format="json")

    def test_authorization_is_enforced(self):
        """Test that the api has user authorization."""

        new_user = User.objects.create(username="hax")
        lesson = Lesson.objects.create(name="TEST",description="This is a test",sensei=new_user)
        new_client = APIClient()
        new_client.force_authenticate(user=new_user)
        change_lesson = {'name': 'Something new', 'description': 'New description'}
        res = self.client.put(
            reverse('lesson', kwargs={'pk': lesson.id}),
            change_lesson, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authentication_is_enforced(self):
        """Test that the api has user authorization."""
        new_client = APIClient()
        res = new_client.get('/lessons/', kwargs={'pk': 2}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_can_get_a_lesson(self):
        """Test the api can get a given lesson."""
        new_user = User.objects.create(username="hax")
        lesson = Lesson.objects.create(name="TESTER", description="This is a test", sensei=new_user,seat_cost=35.00)

        response = self.client.get(
            reverse('lesson',
                    kwargs={'pk': lesson.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, lesson)

    def test_api_can_update_lesson(self):
        """Test the api can update a given lesson."""

        change_lesson = {'name': 'Something new','description':'New description'}
        res = self.client.put(
            reverse('lesson', kwargs={'pk': 1}),
            change_lesson, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_lesson(self):
        """Test the api can delete a lesson."""
        new_user = User.objects.create(username="hax")
        lesson = Lesson.objects.create(name="TESTER", description="This is a test", sensei=new_user)

        response = self.client.delete(
            reverse('lesson', kwargs={'pk': lesson.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
