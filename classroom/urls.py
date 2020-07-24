from django.urls import path, include

def do_nothing(request):
    pass

urlpatterns = [
    path('', do_nothing)
]