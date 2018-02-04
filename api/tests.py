# api test.py

from django.test import TestCase
from .models import Lesson
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


# Create your tests here.
class ModelTestCase(TestCase):
    def setUp(self):
        """Define the for Lesson and other variables"""
        self.name = "My Cool Class"
        self.description = "This is a class for only, if you think you are cool then apply."
        self.lesson = Lesson(name=self.name,description=self.description)

    def test_model_can_create_lesson(self):
        """Test the lesson model can create a lesson."""
        old_count = Lesson.objects.count()
        self.lesson.save()
        new_count = Lesson.objects.count()
        self.assertNotEqual(old_count, new_count)

# Define this after the ModelTestCase
class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.lesson_data = {'name': 'Japanese Class' , 'description':'Join to learn Japanese'}
        self.response = self.client.post(
            reverse('create'),
            self.lesson_data,
            format="json")

    def test_api_can_create_a_lesson(self):
        """Test the api has lesson creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_lesson(self):
        """Test the api can get a given bucketlist."""
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

