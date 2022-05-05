from django.urls import path
from .student_views import StudentCreateView, GetAllProfessorView, StudentRequestView, StudentProfileView
from .professor_views import AddGroupView

urlpatterns = [
    # Student URLs
    path('student/', StudentCreateView.as_view(), name='students'),
    path('get_professors/', GetAllProfessorView.as_view(), name='get_professors'),
    path('student_request/', StudentRequestView.as_view(), name='student_request'),
    path('student_profile/', StudentProfileView.as_view(), name='student_profile'),

    # Professor URLs
    path('add_group/', AddGroupView.as_view(), name='add_group'),
]
