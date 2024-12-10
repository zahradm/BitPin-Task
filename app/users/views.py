from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.users.serializers import UserSerializer, SuperUserSerializer


class BaseRegisterView(APIView):
    serializer_class = None

    def post(self, request, *args, **kwargs):
        if not self.serializer_class:
            return Response(
                {"error": "Serializer class not defined"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(BaseRegisterView):
    serializer_class = UserSerializer


class SuperUserRegisterView(BaseRegisterView):
    serializer_class = SuperUserSerializer
