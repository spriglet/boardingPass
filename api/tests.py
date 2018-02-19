# api test.py

from django.test import TestCase
from .models import Lesson,UserProfile,Seat,TimeSlot,TimeSlotStatus,Transaction,SeatStatus,TransactionStatus
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status




# Create your tests here.
class ModelTestCase(TestCase):
    def setUp(self):
        """Define the for Lesson and other variables"""
        sensei = User.objects.create(username="Sensei")  # ADD THIS LINE
        self.student = User.objects.create(username="Student")
        self.name = "My Cool Class"
        self.description = "This is a class for only, if you think you are cool then apply."
        self.userProfile = UserProfile(user=sensei, company='Test Company',currency='US', country='USA', isSensei=True,timeZone="UTC")
        self.lesson = Lesson(name=self.name,description=self.description,sensei=sensei,length_in_minutes=30)
        self.time_slot_status = TimeSlotStatus(name='Scheduled')

        self.transaction_status = TransactionStatus(name="accepted")
        self.studentProfile = UserProfile(user=self.student,country='Japan')
        self.time_slot_status.save()
        self.time_slot = TimeSlot(start="2018-03-02 10:00", lesson=self.lesson, status=self.time_slot_status)

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
        old_count = Lesson.objects.count()
        self.lesson.save()
        new_count = Lesson.objects.count()
        self.assertNotEqual(old_count, new_count)


    def test_model_can_create_time_slot(self):
        """Test to make can creat time slot record"""
        print(self.lesson.id)
        old_count = TimeSlot.objects.count()
        self.time_slot.save()
        new_count = TimeSlot.objects.count()
        self.assertNotEqual(old_count,new_count)
    def test_model_can_create_student_profile(self):
        """Creates student profile"""
        old_count = UserProfile.objects.count()
        self.studentProfile.save()
        new_count = UserProfile.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_seat(self):
        self.seat = Seat(cost='8.00', status=self.seat_status, student=self.student, time_slot=self.time_slot)
        old_count = Seat.objects.count()
        self.seat.save()
        new_count = Seat.objects.count()
        self.assertNotEqual(old_count,new_count)
    def test_model_can_create_transaction_status(self):
        old_count = TransactionStatus.objects.count()
        self.transaction_status.save()
        new_count = Transactiontatus.objects.count()
        self.assertNotEqual(old_count,new_count)

    def test_model_can_create_transaaction(self):
        """Model to test to see if can create transaction"""
        old_count = Transaction.objects.count()
        self.seat.save()
        transaction = Transaction(amount='8.00',seat=self.seat,status=self.transaction_status)
        transaction.save()
        new_count = Transaction.objects.count()
        self.assertNotEqual(old_count,new_count)


# Define this after the ModelTestCase
class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create(username="nerd")

        # Initialize client and force it to use authentication
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.lesson_data = {'name': 'Japanese Class' , 'description':'Join to learn Japanese','sensei': user.id}
        self.response = self.client.post(reverse('create'), self.lesson_data,format="json")

    def test_api_can_create_a_lesson(self):
        """Test the api has lesson creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_authorization_is_enforced(self):
        """Test that the api has user authorization."""

        new_user = User.objects.create(username="hax")
        lesson = Lesson.objects.create(name="TEST",description="This is a test",sensei=new_user)
        new_client = APIClient()
        new_client.force_authenticate(user=new_user)
        change_lesson = {'name': 'Something new', 'description': 'New description'}
        res = self.client.put(
            reverse('details', kwargs={'pk': lesson.id}),
            change_lesson, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authentication_is_enforced(self):
        """Test that the api has user authorization."""
        new_client = APIClient()
        res = new_client.get('/lessons/', kwargs={'pk': 2}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_UNAUTHORIZED)

    def test_api_can_get_a_lesson(self):
        """Test the api can get a given lesson."""
        lesson = Lesson.objects.get()
        response = self.client.get(
            reverse('details',
                    kwargs={'pk': lesson.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, lesson)

    def test_api_can_update_lesson(self):
        """Test the api can update a given lesson."""
        lesson = Lesson.objects.get()
        change_lesson = {'name': 'Something new','description':'New description'}
        res = self.client.put(
            reverse('details', kwargs={'pk': lesson.id}),
            change_lesson, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_lesson(self):
        """Test the api can delete a lesson."""
        lesson = Lesson.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': lesson.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

