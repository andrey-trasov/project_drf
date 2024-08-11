from rest_framework.serializers import ModelSerializer
from user.models import Payments


class PaymentsSerializer(ModelSerializer):
   class Meta:
       model = Payments
       fields = '__all__'