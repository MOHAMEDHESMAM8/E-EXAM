from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import *
from drf_writable_nested import WritableNestedModelSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('first_name', 'last_name', 'phone',
                    'password', 'email', 'id')


class StudentCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Student
        fields = ['user', 'level']
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        userr = User.objects.create(**user_data)
        return userr
