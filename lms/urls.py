from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.views import (CourseViewSet, LessonCreateApiView, LessonUpdateAPIView, LessonDestroyAPIView,
    LessonRetrieveAPIView, LessonListAPIView)
from lms.apps import LmsConfig

app_name = LmsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson_create/", LessonCreateApiView.as_view(), name="lesson_create"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path("lesson_update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lesson_delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
]


urlpatterns += router.urls

# from lms.apps import LmsConfig
# from rest_framework.routers import DefaultRouter
#
# from lms.views import CourseViewSet
#
# app_name = LmsConfig.name
#
# router = DefaultRouter()
# router.register(r'', CourseViewSet)
#
# urlpatterns = [
#
# ] + router.urls
