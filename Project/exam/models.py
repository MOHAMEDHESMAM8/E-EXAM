from django.db import models
from user.models import Professor, Student, Chapter


class Exam(models.Model):
    LEVEL_ONE = 'F'
    LEVEL_TWO = 'S'
    LEVEL_THREE = 'T'

    LEVEL_CHOICES = [
        (LEVEL_ONE, 'One'),
        (LEVEL_TWO, 'Two'),
        (LEVEL_THREE, 'Three'),
    ]
    professor = models.ForeignKey(
        Professor, on_delete=models.CASCADE, related_name='exam')
    name = models.CharField(max_length=100)
    level = models.CharField(
        max_length=1, choices=LEVEL_CHOICES, default=LEVEL_TWO)
    total = models.PositiveSmallIntegerField()
    time = models.TimeField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)


class ExamOptions(models.Model):
    easy_level = 'E'
    medium_level = 'M'
    hard_level = 'H'

    difficulty_CHOICES = [
        (easy_level, 'Easy'),
        (medium_level, 'Medium'),
        (hard_level, 'Hard'),
    ]
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name='exam_options')
    chapter = models.ForeignKey(Chapter, on_delete=models.PROTECT)
    count = models.PositiveSmallIntegerField()
    difficulty = models.CharField(
        max_length=1, choices=difficulty_CHOICES, default=medium_level)
    updated_at = models.DateTimeField(auto_now=True)


class result(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='result')
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name='result')
    result = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class ExamGroups(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    group = models.ForeignKey(Professor, on_delete=models.PROTECT)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    created_at = models.DateField(auto_now_add=True)
