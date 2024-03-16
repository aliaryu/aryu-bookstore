from .serializers import ContactSerializer
from rest_framework.generics import CreateAPIView


class ContactCreateAPIView(CreateAPIView):
    serializer_class = ContactSerializer
