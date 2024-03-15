from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED
)
from .serializers import UserPassLoginSerializer
from django.contrib.auth import login
from django.utils.translation import gettext_lazy as _


class UserPassAPILoginView(APIView):
    serializer_class = UserPassLoginSerializer

    def post(self, request):
        print(request.data, "*" * 10)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        if user:
            # login(request, user)
            return Response({"message": _("login successfull.")}, status=HTTP_200_OK)
        else:
            return Response({"message": _("invalid username or password.")}, status=HTTP_401_UNAUTHORIZED)


