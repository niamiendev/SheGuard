
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from alert.views import AlertViewSet

router = DefaultRouter()
router.register(r"alerts", AlertViewSet , "alert")

urlpatterns = [
    path("", include(router.urls))
]
