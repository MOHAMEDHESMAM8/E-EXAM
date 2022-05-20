from rest_framework.permissions import IsAuthenticated
from user.models import Chapter
from .models import Exam, ExamOptions
from .serializers import ChaptersSerializers, ExamSerializers, GetCreateExamSerializers, AddExamToGroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch


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


class GetChapterExams(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chapter):
        data = Exam.objects.filter(chapter=chapter)
        serializer = ExamSerializers(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateExam(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GetCreateExamSerializers(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetExam(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, exam):
        exam_obj = Exam.objects.get(pk=exam)
        serializer = GetCreateExamSerializers(exam_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddExamToGroupView(APIView):
    def post(self,request):
        serializer = AddExamToGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(validated_data=request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
