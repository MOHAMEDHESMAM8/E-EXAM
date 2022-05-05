from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Group, Professor, Request
from .serializers import AddGroupSerializer


class AddGroupView(APIView):
    def post(self, request):
        try:
            name = request.data.pop('name')
            professor = Professor.objects.get(user=request.user)
            group = Group.objects.create(name=name, professor=professor)
            group.save()
            return Response('Group is created successfully', status=status.HTTP_200_OK)
        except:
            return Response('Error, please try again', status=status.HTTP_400_BAD_REQUEST)

