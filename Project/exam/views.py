from datetime import datetime
from .serializers import StudentAvailableExamSerializer, StudentExamHistorySerializer, StudentExamDetailsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Exam, ExamGroups, ExamOptions, Result
from question_bank.models import Question
from user.models import Professor_Student, Student
from django.core.exceptions import ObjectDoesNotExist
from user.permissions import IsStudent

class StudentGetExamView(APIView):
    permission_classes = [IsStudent]
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

class StudentAvailableExamView(APIView):
    permission_classes = [IsStudent]
    def get(self, request):
      student_groups = Professor_Student.objects.filter(student=request.user.student).values_list('group', flat=True)
      student_exam = Result.objects.filter(student=request.user.student).values_list('exam', flat=True)
      exams = ExamGroups.objects.filter(group__in=student_groups, start_at__lte = datetime.now(), end_at__gte=datetime.now()).select_related('exam')\
        .exclude(exam__in=student_exam).values('exam', 'exam__name', 
              'exam__time', 'start_at', 'end_at')
      serializer = StudentAvailableExamSerializer(exams, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

class StudentExamHistoryView(APIView):
  permission_classes = [IsStudent]
  def get(self, request):
    exams = Result.objects.select_related('exam').filter(student=request.user.student)\
      .values('exam__name', 'result', 'exam__total', 'exam')
    serializer = StudentExamHistorySerializer(exams, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



class ExamSubmitView(APIView):
  permission_classes=[IsStudent]
  def post(self,request,exam):
    submit_data= request.data
    result = 0
    right_questions=0
    wrong_questions=0
    skipped_questions=0
    exam_professor =  Exam.objects.get(pk=exam).professor
    questions = Question.objects.prefetch_related('answer').filter(professor=exam_professor)

    for obj in submit_data:
      try :
          answer_obj = questions.get(pk=obj.get('question')).answer.get(pk=obj.get('answer'))
          if answer_obj.is_correct:
            result +=1 
            right_questions+=1
          else:
            wrong_questions+=1
      except ObjectDoesNotExist :
          skipped_questions+=1

    set_result =Result()
    set_result.student=request.user.student
    set_result.result=result
    set_result.exam_id=exam
    set_result.save()
    student = Student.objects.get(user=request.user)
    student.rank= result
    student.save()
    
    return Response({"result":result,
    "right_questions":right_questions,
    "wrong_questions":wrong_questions,
    "skipped_questions":skipped_questions}, 
            status=status.HTTP_201_CREATED)


class StudentExamDetailsViewSet(APIView):
  permission_classes=[IsStudent]
  def get(self,request,exam_id):
    exam = Exam.objects.get(id=exam_id)
    student_group = Professor_Student.objects.get(student=request.user.student, professor=exam.professor)
    exam_group = ExamGroups.objects.select_related('exam').filter(exam=exam_id, group=student_group.group)\
      .values('exam', 'exam__name', 'start_at', 'end_at', 'exam__time', 'exam__chapter')
    serializer = StudentExamDetailsSerializer(exam_group, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

