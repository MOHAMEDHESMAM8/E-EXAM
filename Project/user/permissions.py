from rest_framework import permissions
from .models import Professor, Student


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if Student.objects.filter(user=request.user).exists():
              if request.user.role == 'Student':
                if request.method in permissions.SAFE_METHODS:
                  return True
              else: 
                return False
            else:
              return False
        else:
          return False


class IsProfessor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.professor.exists():
              if request.user.role == 'Professor':
                if request.method in permissions.SAFE_METHODS:
                  return True
              else:
                return False
            else:
              return False
        else:
          return False