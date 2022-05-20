from .serializers import ExamOptionsSerializer, ExamSerializers, GetCreateExamSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Exam, ExamOptions
from question_bank.models import Question, Answer

class StudentGetExamView(APIView):
  def get(self, request, exam_id):
    exam_option  = ExamOptions.objects.filter(exam_id=exam_id).values('id', 'chapter', 'difficulty', 'count')
    for obj in exam_option:
      exam = Question.objects.filter()
    return Response('Tmm',status=status.HTTP_200_OK)