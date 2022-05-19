from django.urls import path
from .student_views import StudentCreateView, GetAllProfessorView, StudentRequestView, StudentProfileView
from .professor_views import GetProfessorGroupsView, AddChapterView, GetStudentsRequestView, GroupDetailsView, GetStudentsOfGroupView, GetProfessorStudentsView, AddGroupView, AcceptStudentsRequestsView,  RejectStudentRequestView, GetLevelGroupView, GetProfessorChapterView, LogoutView

urlpatterns = [
    # Student URLs
    path('student/', StudentCreateView.as_view(), name='students'),
    path('get_professors/', GetAllProfessorView.as_view(), name='get_professors'),
    path('student_request/', StudentRequestView.as_view(), name='student_request'),
    path('student_profile/', StudentProfileView.as_view(), name='student_profile'),

    # Professor URLs
    # Levels are F,S,T
    path('professor_groups/<int:level>/', GetProfessorGroupsView.as_view()),
    path('get_student_request/', GetStudentsRequestView.as_view()),
    path('group_details/<int:group_id>/', GroupDetailsView.as_view()),
    path('get_students_group/<int:group_id>/', GetStudentsOfGroupView.as_view()),
    path('professor_students/', GetProfessorStudentsView.as_view()),
    path('add_group/', AddGroupView.as_view()),
    path('accept_student_request/', AcceptStudentsRequestsView.as_view()),
    path('reject_student_request/', RejectStudentRequestView.as_view()),
    path('level_groups/<int:level>/', GetLevelGroupView.as_view()),
    path('level_chapters/<int:level>/', GetProfessorChapterView.as_view()),
    path('chapter/', AddChapterView.as_view(), name='chapter'),
    path('logout/', LogoutView.as_view()),

]
