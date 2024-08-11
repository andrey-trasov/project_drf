from rest_framework.routers import SimpleRouter


from user.views import PaymentsViewSet
from user.apps import UserConfig


app_name = UserConfig.name


router = SimpleRouter()
router.register('', PaymentsViewSet)


urlpatterns = []


urlpatterns += router.urls
