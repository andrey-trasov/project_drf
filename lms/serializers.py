from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson, Subscription
from lms.validators import YoutubeValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YoutubeValidator(field='link_to_video')]


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"  # ('id', 'name', 'description', 'preview')


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