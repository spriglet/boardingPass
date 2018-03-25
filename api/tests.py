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
        lesson.save()
        time_slot = TimeSlot(start="2018-03-02 10:00", lesson=lesson, status=self.time_slot_status)
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

    def test_model_can_create_transaction(self):
        """Test to make can creat time slot record"""
        lesson = Lesson(name=self.name, description=self.description, sensei=self.sensei, length_in_minutes=30,
                        seat_cost=12.00)
        lesson.save()
        time_slot = TimeSlot(start="2018-03-02 10:00", lesson=lesson, status=self.time_slot_status)
        time_slot.save()
        self.seat = Seat(cost=lesson.seat_cost, status=self.seat_status, student=self.student, time_slot=time_slot)
        self.seat.save()
        old_count = Transaction.objects.count()
        self.transaction_status.save()
        transaction = Transaction(status=self.transaction_status,seat=self.seat,amount=15.00)
        transaction.save()
        new_count  = Transaction.objects.count()
        self.assertNotEqual(old_count,new_count)

# Define this after the ModelTestCase
class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.user = User.objects.create(username="nerd")
        # Initialize client and force it to use authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.time_slot_status = TimeSlotStatus(name='Scheduled')
        self.time_slot_status.save()
        self.transaction_status = TransactionStatus(name="accepted")
        self.seat_status = SeatStatus(name="TEST")
        self.seat_status.save()
        self.lesson = Lesson(name='Test Lesson', description='Test', sensei=self.user, length_in_minutes=30)
        self.lesson.save()
        lesson_data = {'name': 'Japanese Class 2', 'description': 'Join to learn Japanese', 'sensei': self.user.id, 'seat_cost':6.50}
        self.response = self.client.post(reverse('create_lesson'), lesson_data)

    def test_api_can_create_a_lesson(self):

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_create_time_slot(self):
        """Test to makes sure user can create time slot"""

        time_slot = {'lesson':self.lesson.id,'start':'2018-03-02 10:00','status':self.time_slot_status.id}
        self.response = self.client.post(reverse('create'),time_slot,format="json")

    def test_api_can_create_seat(self):
        """Test to makes sure user can create time slot"""

        user = User.objects.create(username="Some Student")
        time_slot = TimeSlot(lesson=self.lesson,start='2018-03-02 14:00',status=self.time_slot_status)
        time_slot.save()
        seat_status = SeatStatus(name="TEST")
        seat_status.save()
        seat_data = {'student':user.id,'status':seat_status.id}
        self.response = self.client.post(reverse('create'), seat_data, format="json")

    def test_api_can_create_transaction(self):
        """Test to makes sure can create transaction"""
        user = User.objects.create(username="Some Student")
        time_slot = TimeSlot(lesson=self.lesson, start='2018-03-02 14:00', status=self.time_slot_status)
        time_slot.save()
        seat_status = SeatStatus(name="TEST")
        seat_status.save()
        seat = Seat(cost=self.lesson.seat_cost, status=self.seat_status, student=user, time_slot=time_slot)
        seat.save()
        print(str(self.lesson.seat_cost))
        transaction_data = {'status': self.transaction_status.id,'seat': seat.id,'amount': '10.00'}

        self.response = self.client.post(reverse('create'), transaction_data, format="json")
    def test_authorization_is_enforced(self):
        """Test that the api has user authorization."""

        new_user = User.objects.create(username="hax")

        new_client = APIClient()
        new_client.force_authenticate(user=new_user)
        change_lesson = {'name': 'Something', 'description': 'New description','seat_cost': '100.50','sensei': new_user.id}
        #print(str(new_user))
        #print("lesson Id:"+str(self.lesson.id)+" Lesson user: "+str(self.lesson.sensei))
        res = new_client.put(
            reverse('lesson', kwargs={'pk': self.lesson.id}),
            change_lesson, format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_authentication_is_enforced(self):
        """Test that the api has user authorization."""
        lesson = Lesson.objects.create(name="TEST", description="This is a test", sensei=self.user)
        new_client = APIClient()
        res = new_client.get('/lesson/', kwargs={'pk': lesson.id}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_can_get_a_lesson(self):
        """Test the api can get a given lesson."""
        new_user = User.objects.create(username="hax")
        lesson = Lesson(name="TESTER", description="This is a test", sensei=new_user,seat_cost=35.00)
        lesson.save()
        response = self.client.get(
            reverse('lesson',
                    kwargs={'pk': lesson.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, lesson)

    def test_api_can_update_lesson(self):
        """Test the api can update a given lesson."""
        """Test the api can get a given lesson."""
        new_user = User.objects.create(username="sensei")
        lesson = Lesson(name="Some Name", description="First Description", sensei=new_user, length_in_minutes=30,
                        seat_cost=14.40)
        lesson.save()
        change_lesson = {'name': 'Something new','description':'New description','seat_cost':'20.00'}
        res = self.client.put(
            reverse('lesson', kwargs={'pk': lesson.id}),
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
