from django.shortcuts import render

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .tasks import test

# Create your views here.


class TestApiView(GenericAPIView):

    def get(self, request):
        test.delay()
        return Response("ok", 200)
