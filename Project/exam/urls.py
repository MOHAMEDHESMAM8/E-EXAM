from django.urls import path

from .professor_views import *
from .views import ExamSubmitView, StudentExamDetailsViewSet, StudentGetExamView, StudentAvailableExamView, StudentExamHistoryView
from rest_framework import routers

urlpatterns = [
    path('chapters/<int:level>/', GetProfessorChapters.as_view(), name='Chapters'),
    path('add_exam_group/', AddExamToGroupView.as_view(), name='add_exam_group'),
    path('examResults/<int:exam_id>/', ExamResultView.as_view(), name='get exam result'),
    # Student URLs
    path('student_get_exam/<int:exam_id>/', StudentGetExamView.as_view(), name='student_get_exam'),
    path('student_available_exams/', StudentAvailableExamView.as_view(), name='student_available_exams'),
    path('student_exam_history/', StudentExamHistoryView.as_view(), name='student_exam_history'),
    path('examsubmit/<int:exam>/', ExamSubmitView.as_view(), name='Submit the exam'),
    path('exam_details/<int:exam_id>/', StudentExamDetailsViewSet.as_view(), name='student'),

    
]

router = routers.SimpleRouter()
router.register(r'exam', ExamViewSet,basename='Exam')
urlpatterns += router.urls
