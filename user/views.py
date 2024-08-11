from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from user.models import Payments
from user.serializers import PaymentsSerializer


class PaymentsViewSet(ModelViewSet):
   queryset = Payments.objects.all()
   serializer_class = PaymentsSerializer

   filter_backends = [DjangoFilterBackend,filters.OrderingFilter]    # настройка для сортировки
   filterset_fields = ('paid_lesson', 'paid_course', 'payment_method')    # фильтр
   ordering_fields = ('date_payment',)   # сортировка по дате

