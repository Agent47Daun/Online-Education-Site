from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ClassroomApiView

router = DefaultRouter()
router.register('classroom', ClassroomApiView)


urlpatterns = [
    path('', include(router.urls))
]