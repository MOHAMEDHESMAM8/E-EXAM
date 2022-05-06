from django.urls import path

from .professor_views import *

urlpatterns = [
    path('chapters/<int:level>', GetProfessorChapters.as_view(), name='Chapters'),
    path('exams/<int:chapter>', GetChapterExams.as_view(), name='Chapter Exams'),
    path('createExam/', CreateExam.as_view(), name='Chapter Exams'),

]
