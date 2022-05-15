from requests import request
from .models import Professor_Student, User, Student, Professor
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

# Signals familiar with Observer Design Pattern
@receiver(post_save, sender=User)
def create_new_user(sender, instance ,**kwargs):
    if kwargs['created']:
        if instance.role == 'S':
            Student.objects.create(user=instance)
        elif instance.role == 'P':
            Professor.objects.create(user=instance)


@receiver(pre_save, sender=Professor)
def create_professor_profile(sender, instance, **kwargs):
    user = User.objects.get(id=instance.user_id)
    if user.role == 'S':
        raise ValueError("Add Professor Error")


@receiver(pre_save, sender=Student)
def create_student_profile(sender, instance, **kwargs):
    user = User.objects.get(id=instance.user_id)
    if user.role == 'P':
        raise ValueError("Add Student Error")

