from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class TestView(APIView):

    def get(self, request):
        """
        :param request:
        :return:
        """
        return Response(
            {'detail': 'test'}, status=status.HTTP_200_OK
        )
