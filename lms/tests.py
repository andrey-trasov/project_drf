from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from user.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        """
        создаем бд
        """
        self.user = User.objects.create(email='py.te.2@mail.ru')
        self.course = Course.objects.create(name='Верстка', description='Основы верстки')
        self.lesson = Lesson.objects.create(name='Основы верстки', description='Основы верстки', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)    # авторизовываемся

    def test_lesson_retrieve(self):
        url = reverse('lms:lesson_detail', args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_lesson(self):
        url = reverse('lms:lesson_create')
        # self.client.force_authenticate(user=self.user)
        data = {
            'name': 'New Lesson',
            'description': 'Описание нового урока',
            'course': self.course.pk,
            'owner': self.user.pk
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_update(self):
        url = reverse('lms:lesson_update', args=(self.lesson.pk,))
        data = {
            'name': 'New Lesson 2',
            'description': 'Описание нового урока',
            'course': self.course.pk,
            'owner': self.user.pk
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), 'New Lesson 2')

    def test_lesson_delete(self):
        url = reverse('lms:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse('lms:lesson_list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='py.te.2@mail.ru')
        self.course = Course.objects.create(name='Верстка', description='Основы верстки')
        self.lesson = Lesson.objects.create(name='Основы верстки', description='Основы верстки', course=self.course,
                                            owner=self.user)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        Subscription.objects.all().delete()
        url = reverse('lms:subscription_create')
        data = {'user': self.user.id,
                'course': self.course.id
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_subscription_list(self):
        url = reverse('lms:subscription_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['course'], self.course.id)