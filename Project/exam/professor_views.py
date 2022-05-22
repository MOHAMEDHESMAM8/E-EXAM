from rest_framework.permissions import IsAuthenticated
from user.models import Chapter
from .models import Exam, ExamOptions, Result
from user.models import Student

from .serializers import ChaptersSerializers, ExamResultSerializer, ExamSerializers, GetCreateExamSerializers, AddExamToGroupSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

class GetProfessorChapters(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, level):
        LEVEL_CHOICES = {
            1: 'F',
            2: 'S',
            3: 'T',
        }
        chapters = Chapter.objects.filter(professor=request.user.professor, level=LEVEL_CHOICES[level])
        serializer = ChaptersSerializers(chapters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddExamToGroupView(APIView):
    def post(self,request):
        serializer = AddExamToGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(validated_data=request.data)
        return Response("Exam is Added to Group", status=status.HTTP_200_OK)



class ExamViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Exam.objects.all()

    @action(detail=True, methods=['get'], name='List of Exams')
    def Exams_chapter(self, request, pk=None):
        data = self.queryset.filter(chapter=pk)
        serializer = ExamSerializers(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = GetCreateExamSerializers(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        exam_obj = self.queryset.get(pk=pk)
        serializer = GetCreateExamSerializers(exam_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self,request,pk=None):
        exam = self.queryset.get(pk=pk)
        serializer = GetCreateExamSerializers(exam, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self,request,pk=None):
        exam = self.queryset.get(pk=pk)
        exam.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExamResultView(APIView):
    def get(self,request,exam_id):
        qyeryset = Result.objects.select_related('student__user').filter(exam_id= exam_id)\
        .values('student__user__phone','student__user__first_name','student__user__last_name','student__user__phone','result')
        serilaizer= ExamResultSerializer(qyeryset,many=True)
        return Response(serilaizer.data,status=status.HTTP_200_OK)
