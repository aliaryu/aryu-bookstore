from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST
)
from django.contrib.auth import login
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework import generics, mixins
from .serializers import (
    UserPassLoginSerializer,
    UserSignUpSerializer,
    UserImageSerializer,
    UserInfoSerializer,
    UserAddressSerializer,
    UserPasswordChangeSerializer,
)
from django.contrib.auth import get_user_model
from apps.user.models import Address


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
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserImageSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": True}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserInfoUpdateView(mixins.UpdateModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserInfoSerializer

    def put(self, request, pk):
        return self.update(request, pk)


class UserAddressView(mixins.DestroyModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Address.objects.all()
    serializer_class = UserAddressSerializer

    def post(self, request):
        return self.create(request)

    def delete(self, request, pk):
        return self.destroy(request, pk)


class UserPasswordChangeView(APIView):
    serializer_class = UserPasswordChangeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": _("password changed successfully.")}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
