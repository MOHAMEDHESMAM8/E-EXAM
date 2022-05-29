from rest_framework import permissions
from .models import Professor, Student


class IsStudent(permissions.BasePermission):
  def has_permission(self, request, view):
        if request.user.is_authenticated:
          if Student.objects.filter(user=request.user).exists():
              return True
        return False

class IsProfessor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
          if Professor.objects.filter(user=request.user).exists():
              return True
        return False



