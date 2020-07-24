from django.urls import path, include

from .views import ClassroomCreateListApiView
urlpatterns = [
    path('', ClassroomCreateListApiView.as_view(), name="classroom_list_create")
]