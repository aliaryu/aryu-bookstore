from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST
)
from django.contrib.auth import login
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework import generics, mixins
from .serializers import (
    UserPassLoginSerializer,
    UserSignUpSerializer,
    UserImageSerializer,
    UserInfoSerializer,
)
from django.contrib.auth import get_user_model


User = get_user_model()


class UserPassLoginView(APIView):
    serializer_class = UserPassLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        if user:
            login(request, user)
            return Response({"message": _("login successfull.")}, status=HTTP_200_OK)
        else:
            return Response({"message": _("invalid username or password.")}, status=HTTP_401_UNAUTHORIZED)


class UserSignUpView(CreateAPIView):
    serializer_class = UserSignUpSerializer


class UploadUserImageView(APIView):
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserImageSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": True}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserInfoUpdateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer

    def put(self, request, pk):
        return self.update(request, pk)
