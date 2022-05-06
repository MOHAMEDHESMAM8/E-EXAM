from user.models import Chapter
from .models import Exam
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch


class GetProfessorChapters(APIView):
    def get(self, request, level):

        if level == 1:
            data = Chapter.objects.filter(professor=1, level="F")
        elif level == 2:
            data = Chapter.objects.filter(professor=1, level="S")
        elif level == 3:
            data = Chapter.objects.filter(professor=1, level="T")
        else:
            Response({"level number didn't exists"}, status=status.HTTP_200_OK)
        serializer = chaptersSerializers(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetChapterExams(APIView):
    def get(self, request, chapter):
        data = Exam.objects.filter(chapter=chapter)
        serializer = ExamSerializers(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateExam(APIView):
    def post(self, request):
        serializer = CreateExamSerializers(data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data=request.data, professor=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# if level == 1:
#     data = Chapter.objects.prefetch_related(
#         Prefetch('exam', queryset=Exam.objects.filter(level="F"), to_attr='filtered_exam')
#     ).filter(professor=1)
# elif level == 2:
#     data = Chapter.objects.prefetch_related(
#         Prefetch('exam', queryset=Exam.objects.filter(level="S"), to_attr='filtered_exam')
#     ).filter(professor=1)
# elif level == 3:
#     data = Chapter.objects.prefetch_related(
#         Prefetch('exam', queryset=Exam.objects.filter(level="T"), to_attr='filtered_exam')
#     ).filter(professor=1)
# else:
#     Response({"level number didn't exists"}, status=status.HTTP_400_BAD_REQUEST)
