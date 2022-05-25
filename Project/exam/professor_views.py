from user.models import Chapter
from .models import Exam, ExamOptions, Result
from user.models import Student
from user.permissions import IsStudent, IsProfessor
from .serializers import ChaptersSerializers, CreateExamSerializers, ExamResultSerializer, ExamSerializers, AddExamToGroupSerializer, GetExamSerializers
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

class GetProfessorChapters(APIView):
    permission_classes = [IsProfessor]

    def get(self, request, level):
        LEVEL_CHOICES = {
            1: 'F',
            2: 'S',
            3: 'T',
        }
        chapters = Chapter.objects.filter(professor=request.user.professor, level=LEVEL_CHOICES[level])
        serializer = ChaptersSerializers(chapters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class createExamView(APIView):
    permission_classes = [IsProfessor]

    def post(self, request, level):
        LEVEL_CHOICES = {
            1: 'F',
            2: 'S',
            3: 'T',
        }
        serializer = CreateExamSerializers(data=request.data, context={'request': request,"level":LEVEL_CHOICES[level]})
        if serializer.is_valid():
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ExamViewSet(viewsets.ViewSet):
    # permission_classes = [IsProfessor]
    queryset = Exam.objects.all()

    @action(detail=True, methods=['get'], name='List of Exams')
    def Exams_chapter(self, request, pk=None):
        data = self.queryset.filter(chapter=pk)
        serializer = ExamSerializers(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        exam_obj = self.queryset.select_related('chapter').get(pk=pk)
        serializer = GetExamSerializers(exam_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self,request,pk=None):
        exam = self.queryset.get(pk=pk)
        serializer = CreateExamSerializers(exam, data=request.data)
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


class deleteExamOptions(APIView):
    permission_classes=[IsProfessor]

    def delete(self,request,pk):
        obj = ExamOptions.objects.get(pk=pk)
        obj.delete()
        return Response('done', status=status.HTTP_204_NO_CONTENT)


