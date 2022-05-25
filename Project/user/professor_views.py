from urllib import response
from django.forms import IntegerField, ValidationError
from requests import delete
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Chapter, Group, Professor, Professor_Student, Request, Student
from .serializers import GetStudentRequestSerializer, GroupDetailSerializer, ProfessorRegisterSerializer, UserDataSerializer, ChapterSerializer, GetGroupNameSerializer, GetProfessorStudentsSerializer, AddGroupSerilizer, AcceptStudentRequestSerializer, GetLevelGroupSerializer
from django.http import Http404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser

class GetProfessorGroupsView(APIView):
    def get(self, request, level):
        LEVEL_CHOICES = {
            1: 'F',
            2: 'S',
            3: 'T',
        }
        results = []
        group = Group.objects.filter(professor=request.user.professor, level=LEVEL_CHOICES[level]).values('id','name', 'created_at')
        for obj in group:
            student = Professor_Student.objects.filter(professor=request.user.professor, group=obj['id']).count()
            object ={'id':obj['id'], 'name':obj['name'], 'created_at':obj['created_at'], 'student_count':student}
            results.append(object)
        return Response(results, status=status.HTTP_200_OK)


class AddGroupView(APIView):
    def post(self, request,level):
        LEVEL_CHOICES = {
            1: 'F',
            2: 'S',
            3: 'T',
        }
        serializer = AddGroupSerilizer(
            data=request.data, context={'request': request, 'level':LEVEL_CHOICES[level]})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise Http404

    def get(self, request, group_id):
        group = self.get_object(group_id)
        serializer = GetGroupNameSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, group_id):
        group = self.get_object(group_id)
        serializer = GroupDetailSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, group_id):
        group = self.get_object(group_id)
        students_group = Professor_Student.objects.filter(group=group)
        if students_group:
            return Response("Group is not empty", status=status.HTTP_400_BAD_REQUEST)
        group.delete()
        return Response('Group is deleted successfully', status=status.HTTP_204_NO_CONTENT)


class GetStudentsOfGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        students = Professor_Student.objects.select_related('student').filter(group=group_id).values(
            'student__user__first_name', 'student__user__last_name', 'student__user__email', 'student__user__phone', 'student')
        serializer = GetStudentRequestSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetStudentsRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,level):
        LEVEL_CHOICES = {
            1: 'F',
            2: 'S',
            3: 'T',
        }
        requests = Request.objects.select_related('student').filter(professor__user=request.user,student__level=LEVEL_CHOICES[level]).values(
            'student', 'student__user__email', 'student__user__first_name', 'student__user__last_name', 'student__user__phone')
        serializer = GetStudentRequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProfessorStudentsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, level):
        LEVEL_CHOICES = {
            1: 'F',
            2: 'S',
            3: 'T',
        }
        students = Professor_Student.objects.select_related('students','group')\
            .filter(professor=request.user.professor,student__level =LEVEL_CHOICES[level])\
            .values('student', 'student__user__email', 'student__user__first_name', 'student__user__last_name', 'student__user__phone', 'group__name')
        serializer = GetProfessorStudentsSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AcceptStudentsRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AcceptStudentRequestSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeStudentGroupView(APIView):
    def get_object(self, student_id):
        try:
            return Professor_Student.objects.get(student=student_id)
        except Professor_Student.DoesNotExist:
            raise Http404
    
    def validate_ids(self, id_list):
        for id in id_list:
            try:
                Professor_Student.objects.get(id=id)
            except (Professor_Student.DoesNotExist, ValidationError):
                return Response("Error, please try again", status=status.HTTP_400_BAD_REQUEST)
        return True
    def put(self,request):
        students = request.data['students']
        self.validate_ids(id_list=students)
        for student in students:
            obj = self.get_object(student)
            obj.group_id = request.data['group']
            obj.save()
        return Response("The Student Group is changed", status=status.HTTP_200_OK)



class RejectStudentRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if all(isinstance(x, int) for x in request.data):
            for student in request.data:
                student_request = Request.objects.get(student=student, professor=request.user.professor)
                student_request.delete()
            return Response("Student Request is Rejected", status=status.HTTP_200_OK)
        return Response("Error, please try again", status=status.HTTP_400_BAD_REQUEST)


class GetLevelGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, level):
        LEVEL_CHOICES = {
            1: 'F',
            2: 'S',
            3: 'T',
        }
        groups = Group.objects.filter(
            level=LEVEL_CHOICES[level], professor=request.user.professor)
        serializer = GetLevelGroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProfessorChapterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, level):
        LEVEL_CHOICES = {
            1: 'F',
            2: 'S',
            3: 'T',
        }
        chapters = Chapter.objects.filter(
            professor=request.user.professor, level=LEVEL_CHOICES[level])
        serializer = GetLevelGroupSerializer(chapters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddChapterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chapters = Chapter.objects.filter(professor=request.user.professor)
        serializer = ChapterSerializer(chapters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ChapterSerializer(data=request.data, context={
            'request': request.user.professor})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class StudentRank(APIView):
    def get(self, request,level):
        LEVEL_CHOICES = {
            1: 'F',
            2: 'S',
            3: 'T',
        }
        students = Student.objects.select_related('user').filter(level=LEVEL_CHOICES[level]).order_by('-score')[:3]\
        .values('user__first_name', 'user__last_name')
        serializer = UserDataSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfessorRegisterView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, format=None):
        serializer = ProfessorRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class deleteStudentsView(APIView):
    def delete(self,request):
        data = request.data
        for id in data:
            obj = Professor_Student.objects.get(student__id =id,professor=request.user.professor)
            obj.delete()
        return Response("done",status=status.HTTP_204_NO_CONTENT)
