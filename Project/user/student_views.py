from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Professor, Request, Student, Professor_Level, User
from .serializers import StudentCreateSerializer, GetAllProfessorsSerializer, StudentProfileSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404


class StudentCreateView(APIView):
    def post(self, request):
        serializer = StudentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetAllProfessorView(APIView):
    def get(self, request):
        student = Student.objects.get(user=request.user)
        professors = Professor_Level.objects.select_related('professor').filter(level=student.level).values(
            'professor__user__id', 'professor__user__first_name', 'professor__user__last_name', 'professor__avatar')
        serializer = GetAllProfessorsSerializer(professors, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentRequestView(APIView):
    def post(self, request):
        try:
            professor = request.data.pop('professor')
            student = Student.objects.get(user=request.user)
            student_request = Request.objects.create(
                professor_id=professor, student_id=student.id)
            student_request.save()
            return Response('Request is sent successfully', status=status.HTTP_200_OK)
        except:
            return Response('Error, please try again', status=status.HTTP_400_BAD_REQUEST)


class StudentProfileView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request):
        user = self.get_object(request.user.id)
        serializer = StudentProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = self.get_object(request.user.id)
        serializer = StudentProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
