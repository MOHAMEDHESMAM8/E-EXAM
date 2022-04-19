from django.urls import path
from .student_views import StudentView

urlpatterns = [
    path('student/', StudentView.as_view(), name='students'),
]
