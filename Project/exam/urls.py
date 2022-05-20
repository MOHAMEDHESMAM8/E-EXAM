from django.urls import path

from .professor_views import *
from .views import StudentGetExamView

urlpatterns = [
    path('chapters/<int:level>', GetProfessorChapters.as_view(), name='Chapters'),
    path('exams/<int:chapter>/', GetChapterExams.as_view(), name='Chapter Exams'),
    path('createExam/', CreateExam.as_view(), name='Chapter Exams'),
    
    # Student URLs
    path('student_get_exam/<int:exam_id>/', StudentGetExamView.as_view(), name='student_get_exam'),

]