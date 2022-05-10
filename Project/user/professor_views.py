from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Group, Professor, Professor_Student, Request, Student
from .serializers import GetStudentRequestSerializer, GetGroupDataSerailizer, GroupDetailSerializer, GetGroupNameSerializer, GetProfessorStudentsSerializer, AddGroupSerilizer
from django.db.models import Count
from django.http import Http404


class GetProfessorGroupsView(APIView):
    def get(self, request, level):
        groups = Professor_Student.objects.filter(professor__user=request.user, group__level=level).values(
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


# class AddStudentToGroupView(APIView):
#     def post(self, request):

class GetProfessorStudentView(APIView):
    def get(self, request):
        groups = Group.objects.filter(
            professor__user=request.user).values('id')
        students = Professor_Student.objects.select_related('students').filter(group__in=groups).values(
            'student', 'student__user__email', 'student__user__first_name', 'student__user__last_name', 'student__user__phone', 'group__name')
        serializer = GetProfessorStudentsSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class AcceptStudentsRequests(APIView):
#     def post(self, request):
