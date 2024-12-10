from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create_user(self, validated_data, is_superuser=False):
        if is_superuser:
            return User.objects.create_superuser(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )


class UserSerializer(BaseUserSerializer):
    def create(self, validated_data):
        return self.create_user(validated_data)


class SuperUserSerializer(BaseUserSerializer):
    def create(self, validated_data):
        return self.create_user(validated_data, is_superuser=True)
