from dataclasses import fields
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import Group, User, Student, Professor, Request
from drf_writable_nested import WritableNestedModelSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('first_name', 'last_name',
                'phone', 'password', 'email', 'id')


class StudentCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Student
        fields = ['user', 'level']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        level = validated_data.pop('level')
        user = User.objects.create(**user_data)
        student = Student.objects.get(user=user)
        student.level = level
        student.save()
        return student


class GetAllProfessorsSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='professor__user__id')
    first_name = serializers.CharField(
        max_length=255, source='professor__user__first_name')
    last_name = serializers.CharField(
        max_length=255, source='professor__user__last_name')
    avatar = serializers.CharField(max_length=255, source='professor__avatar')

class StudentProfileSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=11)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('last_name', instance.phone)
        instance.save()
        return instance

# Professor Serializer


class AddGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['professor', 'name']