from asyncore import read
from dataclasses import fields
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import Group, Professor_Student, User, Student, Professor, Request, Chapter
from django.contrib.auth.hashers import make_password


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('first_name', 'last_name', 'phone', 'password', 'email', 'id')


class StudentCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Student
        fields = ['user', 'level']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        level = validated_data.pop('level')
        user_data['password'] = make_password(user_data['password'])
        user = User.objects.create(**user_data, role='S')
        student = Student.objects.get(user=user)
        student.level = level
        student.save()
        return student


class GetMyProfessorsSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='professor')
    first_name = serializers.CharField(
        max_length=255, source='professor__user__first_name')
    last_name = serializers.CharField(
        max_length=255, source='professor__user__last_name')
    avatar = serializers.CharField(max_length=255, source='professor__avatar')

class GetAllProfessorsSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='professor')
    first_name = serializers.CharField(
        max_length=255, source='professor__user__first_name')
    last_name = serializers.CharField(
        max_length=255, source='professor__user__last_name')
    avatar = serializers.CharField(max_length=255, source='professor__avatar')
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        student = self.context['request'].user.student
        requests = Request.objects.filter(
            student=student, professor=obj['professor'])
        if requests.exists():
            data = {
                'status': 'Pending'
            }
        else:
            data = {
                'status': 'Join'
            }
        return data


class StudentProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=11)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.phone = validated_data.get('last_name', instance.phone)
        instance.save()
        return instance


class StudentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['professor']

    def create(self, validated_data):
        request = Request()
        request.professor = validated_data.pop('professor')
        request.student = self.context['request'].user.student
        request.save()
        return request

class UserDataSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255, source='user__first_name')
    last_name = serializers.CharField(max_length=255, source='user__last_name')

# Professor Serializer


class GetStudentRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='student')
    first_name = serializers.CharField(
        max_length=255, source='student__user__first_name')
    last_name = serializers.CharField(
        max_length=255, source='student__user__last_name')
    email = serializers.CharField(
        max_length=255, source='student__user__email')
    phone = serializers.CharField(
        max_length=255, source='student__user__phone')


class GetGroupNameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    id = serializers.IntegerField()


class AddGroupSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'id']

    def create(self, validated_data):
        group = Group()
        group.name = validated_data.pop('name')
        group.level = self.context['level']
        group.professor = self.context['request'].user.professor
        group.save()
        return group


class GroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'id']


class GetProfessorStudentsSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='student')
    first_name = serializers.CharField(
        max_length=255, source='student__user__first_name')
    last_name = serializers.CharField(
        max_length=255, source='student__user__last_name')
    email = serializers.CharField(
        max_length=255, source='student__user__email')
    phone = serializers.CharField(
        max_length=255, source='student__user__phone')
    group = serializers.CharField(max_length=255, source='group__name')


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'name', 'level']

    def create(self, validated_data):
        chapter = Chapter()
        chapter.name = validated_data.pop('name')
        chapter.level = validated_data.pop('level')
        chapter.professor = self.context['request']
        chapter.save()
        return chapter


class AcceptStudentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor_Student
        fields = ['group']

    def create(self, validated_data):
        students = self.context['request'].data['students']
        group = validated_data.pop('group')
        for obj in students:
            professor = self.context['request'].user.professor
            student_group = Professor_Student.objects.create(student_id=obj, professor=professor, group_id=group.id)
            request = Request.objects.get(student_id=obj, professor=professor)
            request.delete()
        return student_group
    


class GetLevelGroupSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)


class ProfessorRegisterSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()
    class Meta:
        model = Professor
        fields = ['user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        print(user_data)
        user_data['password'] = make_password(user_data['password'])
        user = User.objects.create(is_active=False, role='P', **validated_data)
        professor = Professor.objects.get(user=user)
        professor.save()
        return professor
