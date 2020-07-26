from django.urls import path, include

from .views import ClassroomCreateListApiView, ClassroomAddLesson, ClassroomRetrieveUpdateDestroyApiView, RetrieveUpdateDestroyApiView
urlpatterns = [
    path('', ClassroomCreateListApiView.as_view(), name="classroom_list_create"),
    path('<int:pk>/', ClassroomRetrieveUpdateDestroyApiView.as_view(), name="classroom_retrieve_update_destroy"),
    path('<int:pk>/add_lesson/', ClassroomAddLesson.as_view(), name="classroom_add_lesson"),
    path("lesson/<int:pk>/", RetrieveUpdateDestroyApiView.as_view(), name="classroom_lesson_retrieve_update_destroy")
]