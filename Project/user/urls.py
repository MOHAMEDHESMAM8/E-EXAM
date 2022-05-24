from django.urls import path
from .student_views import StudentCreateView, GetAllProfessorView, StudentRequestView, StudentProfileView, GetStudentProfessorView
from .professor_views import GetProfessorGroupsView, ChangeStudentGroupView, ProfessorRegisterView, GetProfessorStudentsView, StudentRank, AddChapterView, GetStudentsRequestView, GroupDetailsView, GetStudentsOfGroupView, AddGroupView, AcceptStudentsRequestsView,  RejectStudentRequestView, GetLevelGroupView, GetProfessorChapterView, LogoutView, deleteStudentsView

urlpatterns = [
    # Student URLs
    path('student/', StudentCreateView.as_view(), name='students'),
    path('get_professors/', GetAllProfessorView.as_view(), name='get_professors'),
    path('student_request/', StudentRequestView.as_view(), name='student_request'),
    path('student_profile/', StudentProfileView.as_view(), name='student_profile'),
    path('logout/', LogoutView.as_view()),
    path('student_professors/', GetStudentProfessorView.as_view(), name='student_professors'),

    # Professor URLs
    # Levels are F,S,T
    path('professor_groups/<int:level>/', GetProfessorGroupsView.as_view()),
    path('get_student_request/<int:level>/', GetStudentsRequestView.as_view()),
    path('group_details/<int:group_id>/', GroupDetailsView.as_view()),
    path('get_students_group/<int:group_id>/', GetStudentsOfGroupView.as_view()),
    path('professor_students/<int:level>/', GetProfessorStudentsView.as_view()),
    path('add_group/', AddGroupView.as_view()),
    path('accept_student_request/', AcceptStudentsRequestsView.as_view()),
    path('reject_student_request/', RejectStudentRequestView.as_view()),
    path('level_groups/<int:level>/', GetLevelGroupView.as_view()),
    path('level_chapters/<int:level>/', GetProfessorChapterView.as_view()),
    path('chapter/', AddChapterView.as_view(), name='chapter'),
    path('change_student_group/', ChangeStudentGroupView.as_view(), name='change_student_group/'),
    path('student_level_ranks/<int:level>/', StudentRank.as_view(), name='student_level_ranks'),
    path('professor_register/', ProfessorRegisterView.as_view()),
    path('deletestudents/', deleteStudentsView.as_view()),


]
