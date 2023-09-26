from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.authentication import initiate_auth, set_password
from users.models import User
from users.serializers import (
    CustomLoginResultSerializer,
    CustomLoginSerializer,
    UserSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):
    def get_serializer(self, *args, **kwargs):
        return CustomLoginSerializer(*args, **kwargs)

    @swagger_auto_schema(responses={200: CustomLoginResultSerializer})
    def post(self, request):
        input_serializer = CustomLoginSerializer(request.data)
        username = input_serializer.data["username"]
        password = input_serializer.data["password"]
        result = initiate_auth(username, password)
        data = {"token": result["AuthenticationResult"]["AccessToken"]}
        print("Data:", data)
        serializer2 = CustomLoginResultSerializer(data)
        return Response(serializer2.data)


class SetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        return CustomLoginSerializer(*args, **kwargs)

    def post(self, request):
        input_serializer = CustomLoginSerializer(request.data)
        username = input_serializer.data["username"]
        password = input_serializer.data["password"]
        result = set_password(username, password)
        return Response(result)
