from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Subscription
from lms.paginators import CustomPagination
from lms.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer,
    SubscriptionSerializer,
)
from user.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":  # если детальный просмотр 1 курса
            return CourseDetailSerializer
        return CourseSerializer

    # присваиваем owner при создании
    def perform_create(self, serializer):
        course = serializer.save()  # сохраняем
        course.owner = self.request.user
        course.save()

    # проверяем состоит ли пользоватеь в группе moders
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerator,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner | ~IsModerator,)
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()  # сохраняем
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModerator | IsOwner)


class SubscriptionCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user  # получаем пользователя
        course_id = self.request.data.get("course")  # получаем id курса
        course = get_object_or_404(
            Course, pk=course_id
        )  # получаем объект курса из базы с помощью
        subs_item = Subscription.objects.filter(
            user=user, course=course
        )  # получаем объекты подписок по текущему пользователю и курса
        if (
            subs_item.exists()
        ):  # Если подписка у пользователя на этот курс есть - удаляем ее
            subs_item.delete()
            message = "Подписка удалена"
        else:  # Если подписки у пользователя на этот курс нет - создаем ее
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"
        return Response({"message": message}, status=status.HTTP_201_CREATED)


class SubscriptionListAPIView(ListAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
