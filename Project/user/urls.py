from django.urls import path
from .student_views import StudentCreateView, GetAllProfessorView, StudentRequestView, StudentProfileView
from .professor_views import GroupView, GetStudentsRequestView, GroupDetailsView, GetStudentsOfGroupView, GetProfessorStudentView

urlpatterns = [
    # Student URLs
    path('student/', StudentCreateView.as_view(), name='students'),
    path('get_professors/', GetAllProfessorView.as_view(), name='get_professors'),
    path('student_request/', StudentRequestView.as_view(), name='student_request'),
    path('student_profile/', StudentProfileView.as_view(), name='student_profile'),

    # Professor URLs
    # Levels are F,S,T
    path('group/<str:level>', GroupView.as_view(), name='add_group'),
    path('get_student_request/', GetStudentsRequestView.as_view(),name='get_student_request'),
    path('group_details/<int:group_id>/', GroupDetailsView.as_view(), name='group_details'),
    path('get_students_group/<int:group_id>', GetStudentsOfGroupView.as_view(), name='get_students_group'),
    path('professor_students/',GetProfessorStudentView.as_view(), name='professor_students')
    
]
