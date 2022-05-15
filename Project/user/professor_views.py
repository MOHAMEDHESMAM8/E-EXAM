from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Chapter, Group, Professor_Student, Request
from .serializers import GetStudentRequestSerializer, GetGroupDataSerailizer, GroupDetailSerializer, ChapterSerializer, GetGroupNameSerializer, GetProfessorStudentsSerializer, AddGroupSerilizer, AcceptStudentRequestSerializer, GetLevelGroupSerializer
from django.db.models import Count
from django.http import Http404
from rest_framework_simplejwt.tokens import RefreshToken


class GetProfessorGroupsView(APIView):
    def get(self, request, level):
        LEVEL_CHOICES = {
            1: 'F',
            2: 'S',
            3: 'T',
        }
        groups = Professor_Student.objects.filter(professor__user=request.user, group__level=LEVEL_CHOICES[level]).values(
            'group__name', 'group__created_at', 'group__id').annotate(student_count=Count('student'))
        serializer = GetGroupDataSerailizer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddGroupView(APIView):
    def post(self, request):
        serializer = AddGroupSerilizer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetailsView(APIView):
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
    def get(self, request, group_id):
        students = Professor_Student.objects.select_related('student').filter(group=group_id).values(
            'student__user__first_name', 'student__user__last_name', 'student__user__email', 'student__user__phone', 'student')
        serializer = GetStudentRequestSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetStudentsRequestView(APIView):
    def get(self, request):
        requests = Request.objects.select_related('student').filter(professor__user=request.user).values(
            'student', 'student__user__email', 'student__user__first_name', 'student__user__last_name', 'student__user__phone')
        serializer = GetStudentRequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProfessorStudentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = Group.objects.filter(
            professor__user=request.user).values('id')
        students = Professor_Student.objects.select_related('students').filter(group__in=groups).values(
            'student', 'student__user__email', 'student__user__first_name', 'student__user__last_name', 'student__user__phone', 'group__name')
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


class RejectStudentRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if all(isinstance(x, int) for x in request.data):
            for student in request.data:
                student_request = Request.objects.get(
                    student=student, professor=request.user.professor)
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
