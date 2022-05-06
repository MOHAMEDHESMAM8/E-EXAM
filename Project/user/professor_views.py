from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Group, Professor, Request, GroupStudents, Student
from .serializers import GetStudentRequestSerializer, GetGroupDataSerailizer, GroupDetailSerializer, GetGroupNameSerializer, GetStudentsGroupSerializer
from django.db.models import Count
from django.http import Http404


class GroupView(APIView):
    def get(self, request, level):
        groups = GroupStudents.objects.filter(group__professor__user=request.user, group__level=level).values(
            'group__name', 'group__created_at', 'group__id').annotate(student_count=Count('student'))
        serializer = GetGroupDataSerailizer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            name = request.data.pop('name')
            professor = Professor.objects.get(user=request.user)
            group = Group.objects.create(name=name, professor=professor)
            group.save()
            return Response('Group is created successfully', status=status.HTTP_200_OK)
        except:
            return Response('Error, please try again', status=status.HTTP_400_BAD_REQUEST)


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
        students_group = GroupStudents.objects.filter(group=group)
        if students_group:
            return Response("Group is not empty", status=status.HTTP_400_BAD_REQUEST)
        group.delete()
        return Response('Group is deleted successfully', status=status.HTTP_204_NO_CONTENT)


class GetStudentsGroupView(APIView):
    def get(self, request, group_id):
        students = GroupStudents.objects.select_related('student').filter(group=group_id).values(
            'student__user__first_name', 'student__user__last_name', 'student__user__email', 'student__user__phone')
        serializer = GetStudentsGroupSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetStudentRequestView(APIView):
    def get(self, request):
        requests = Request.objects.select_related('student').filter(professor__user=request.user).values(
            'student', 'student__user__email', 'student__user__first_name', 'student__user__last_name', 'student__user__phone')
        serializer = GetStudentRequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# class AddStudentToGroupView(APIView):
#     def post(self, request):
