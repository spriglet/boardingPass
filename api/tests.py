# api test.py

from django.test import TestCase
from .models import Lesson

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




