from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.product.models import Book, Author
from apps.comment.models import Comment
from rest_framework.permissions import IsAuthenticated
from .serializers import CommentSerializer
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


class SaveUnsaveBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            user = request.user

            if user in book.saves.all():
                book.saves.remove(user)
                action = 'unsave'
            else:
                book.saves.add(user)
                action = 'save'

            if action == "unsave":
                return Response({"unsave": True}, status=status.HTTP_200_OK)
            elif action == "save":
                return Response({"save": True}, status=status.HTTP_200_OK)
            
        except Book.DoesNotExist:
            return Response({"error": _("book not found.")}, status=status.HTTP_404_NOT_FOUND)


class CommentBookAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request, pk):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            book = Book.objects.get(pk=pk)
            Comment.objects.create(
                user = request.user,
                text = serializer.validated_data['message'],
                content_object = book
            )
            return Response({"comment": True}, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({"error": _("book not found.")}, status=status.HTTP_404_NOT_FOUND)
        

class CommentAuthorAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request, pk):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            author = Author.objects.get(pk=pk)
            Comment.objects.create(
                user = request.user,
                text = serializer.validated_data['message'],
                content_object = author
            )
            return Response({"comment": True}, status=status.HTTP_200_OK)
        except Author.DoesNotExist:
            return Response({"error": _("author not found.")}, status=status.HTTP_404_NOT_FOUND)
