from rest_framework.routers import SimpleRouter
from user.views import PaymentsViewSet, PaymentsCreateAPIView
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.apps import UserConfig
from user.views import UserCreateAPIView

app_name = UserConfig.name

router = SimpleRouter()
router.register("", PaymentsViewSet)

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("course_purchase/", PaymentsCreateAPIView.as_view(), name="course_purchase"),
]

urlpatterns += router.urls
