from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.product.models import Book
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _


class LikeUnlikeBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            user = request.user

            if user in book.likes.all():
                book.likes.remove(user)
                action = 'unlike'
            else:
                book.likes.add(user)
                action = 'like'

            if action == "unlike":
                return Response({"unlike": True}, status=status.HTTP_200_OK)
            elif action == "like":
                return Response({"like": True}, status=status.HTTP_200_OK)
            
        except Book.DoesNotExist:
            return Response({"error": _("book not found.")}, status=status.HTTP_404_NOT_FOUND)
