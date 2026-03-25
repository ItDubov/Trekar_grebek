from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from habits.models import Habit
from datetime import time

class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="123")

    def test_create_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Home",
            action="Exercise",
            time=time(7,0),
            execution_time=10,
            period_days=1
        )
        self.assertEqual(str(habit), "Exercise")
        self.assertTrue(habit.is_active)

    def test_invalid_related_habit_and_reward(self):
        pleasant = Habit.objects.create(
            user=self.user,
            place="Home",
            action="Read book",
            time=time(8,0),
            execution_time=5,
            is_pleasant=True
        )
        habit = Habit(
            user=self.user,
            place="Gym",
            action="Workout",
            time=time(9,0),
            execution_time=15,
            reward="Candy",
            related_habit=pleasant
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

class HabitViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="viewuser", password="123")
        self.client.login(username="viewuser", password="123")
        for i in range(10):
            Habit.objects.create(
                user=self.user,
                place="Home",
                action=f"Action {i}",
                time=time(7,0),
                execution_time=5,
                period_days=1
            )

    def test_list_habits_pagination(self):
        url = reverse("habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)

    def test_create_habit(self):
        url = reverse("habit-list")
        data = {
            "place": "Office",
            "action": "Meditate",
            "time": "08:00:00",
            "execution_time": 10,
            "period_days": 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class HabitPermissionTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="123")
        self.user2 = User.objects.create_user(username="user2", password="123")
        self.habit = Habit.objects.create(
            user=self.user1,
            place="Home",
            action="Action1",
            time=time(7,0),
            execution_time=5,
            period_days=1
        )

    def test_user_cannot_edit_others_habit(self):
        self.client.login(username="user2", password="123")
        url = f"/habits/{self.habit.id}/"
        response = self.client.put(url, {"action": "Hack"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
