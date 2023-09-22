from rest_framework import serializers

from users.models import User


class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)


class CustomLoginResultSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=1024)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
