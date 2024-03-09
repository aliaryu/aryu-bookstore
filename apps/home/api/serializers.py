from rest_framework import serializers
from apps.home.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'text']
