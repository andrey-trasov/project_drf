from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from user.models import Payments, User
from user.serializers import PaymentsSerializer, UserSerializer
from user.services import create_stripe_prise, create_stripe_session


class PaymentsViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]  # настройка для сортировки
    filterset_fields = ("paid_lesson", "paid_course", "payment_method")  # фильтр
    ordering_fields = ("date_payment",)  # сортировка по дате


class UserCreateAPIView(CreateAPIView):
    """
    Интпоинт для регистрации пользователя
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)  # открываем для анонимных пользователей

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)  # сохраняяем пользователя активным
        user.set_password(user.password)  # хэшируем пароль
        user.save()

class PaymentsCreateAPIView(CreateAPIView):
    """
    Интпоинт для оплаты
    """

    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        price = create_stripe_prise(payment.payment_sum)
        session_id, payment_link = create_stripe_session(price.id)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


