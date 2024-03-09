from rest_framework import status
from .serializers import ContactSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


class ContactCreateAPIView(CreateAPIView):
    serializer_class = ContactSerializer
