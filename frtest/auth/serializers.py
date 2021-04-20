from rest_framework import serializers

from .auth import auth


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
