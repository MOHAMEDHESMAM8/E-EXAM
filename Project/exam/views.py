from .serializers import ExamOptionsSerializer, ExamSerializers, GetCreateExamSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Exam, ExamOptions
from question_bank.models import Question, Answer


class StudentGetExamView(APIView):
  def get(self, request, exam_id):
    exam_option  = ExamOptions.objects.select_related('exam').filter(exam_id=exam_id).values(
        'chapter', 'difficulty', 'count', 'exam__level')
    questions_data = []
    for obj in exam_option:
      questions = list(Question.objects \
      .prefetch_related('answer') \
      .filter(chapter=obj['chapter'], level=obj['exam__level'], difficulty=obj['difficulty'])\
      .order_by('?')[:obj['count']]
      )
      for i in range(0,len(questions)):
            obj = {
              'id': questions[i].id,
              'text':questions[i].text,
              'answers':list(questions[i].answer.all().order_by('?').values('id', 'answer', 'is_correct')),
            }
            questions_data.append(obj)
    return Response(questions_data, status=status.HTTP_200_OK)