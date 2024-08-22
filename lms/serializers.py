from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson, Subscription
from lms.validators import YoutubeValidator
from rest_framework import serializers


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YoutubeValidator(field='link_to_video')]


class CourseSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()
    class Meta:
        model = Course
        # fields = "__all__"  # ('id', 'name', 'description', 'preview')
        fields = ('id', 'name', 'description', 'preview', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user    # достаем юзера
        if user.is_authenticated:    # если аутенцифицирован
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False



class CourseDetailSerializer(ModelSerializer):
    number_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_number_lessons(self, instance):
        # return Lesson.objects.filter(course=course).count()
        return instance.lessons.count()  # lesson_set

    class Meta:
        model = Course
        fields = ("id", "name", "description", "preview", "number_lessons", "lessons")

class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'