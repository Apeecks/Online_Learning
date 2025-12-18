from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from materials.models import Course, Lesson, CourseSubscription

User = get_user_model()


class LessonCrudAndSubscriptionTests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@mail.ru",
            password="Pass12345!"
        )
        self.other = User.objects.create_user(
            email="other@mail.ru",
            password="Pass12345!"
        )
        self.moder = User.objects.create_user(
            email="moder@mail.ru",
            password="Pass12345!"
        )

        moderators, _ = Group.objects.get_or_create(name="moderators")
        self.moder.groups.add(moderators)

        self.course = Course.objects.create(
            title="Test course",
            description="Desc",
            owner=self.owner
        )

        self.lesson = Lesson.objects.create(
            title="Test lesson",
            description="Lesson desc",
            url="https://youtube.com",
            course=self.course,
            owner=self.owner,
        )

    def test_owner_can_create_lesson(self):
        self.client.force_authenticate(user=self.owner)

        data = {
            "title": "New lesson",
            "description": "ok",
            "url": "https://youtube.com",
            "course": self.course.id,
        }

        response = self.client.post("/lesson/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_moderator_cannot_create_lesson(self):
        self.client.force_authenticate(user=self.moder)

        data = {
            "title": "New lesson",
            "description": "ok",
            "url": "https://youtube.com",
            "course": self.course.id,
        }

        response = self.client.post("/lesson/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_user_cannot_view_lesson(self):
        self.client.force_authenticate(user=self.other)

        response = self.client.get(f"/lesson/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_moderator_can_view_any_lesson(self):
        self.client.force_authenticate(user=self.moder)

        response = self.client.get(f"/lesson/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_can_update_lesson(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            f"/lesson/update/{self.lesson.id}/",
            {"title": "Updated"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_can_delete_lesson(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(f"/lesson/delete/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_subscription_toggle(self):
        self.client.force_authenticate(user=self.other)

        # подписка
        response = self.client.post(
            "/courses/subscription/",
            {"course_id": self.course.id},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            CourseSubscription.objects.filter(
                user=self.other,
                course=self.course
            ).exists()
        )

        # отписка
        response = self.client.post(
            "/courses/subscription/",
            {"course_id": self.course.id},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            CourseSubscription.objects.filter(
                user=self.other,
                course=self.course
            ).exists()
        )
