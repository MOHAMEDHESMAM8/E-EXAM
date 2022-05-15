from django.urls import path
from .views import AddQuestionView, GetQuestionView,QuestionDetialsView

urlpatterns = [
    path('add_question/', AddQuestionView.as_view()),
    path('get_questions/<int:level>', GetQuestionView.as_view()),
    path('question_details/<int:id>', QuestionDetialsView.as_view()),

]
