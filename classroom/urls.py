from django.urls import path, include

from .views import ClassroomCreateListApiView, ClassroomAddLesson
urlpatterns = [
    path('', ClassroomCreateListApiView.as_view(), name="classroom_list_create"),
    path('<int:id>/add_lesson/', ClassroomAddLesson.as_view(), name="classroom_add_lesson")
]