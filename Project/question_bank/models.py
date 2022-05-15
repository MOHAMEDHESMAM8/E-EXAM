from django.db import models
from user.models import  Chapter, Professor



class Question(models.Model):
    easy_level = 'E'
    medium_level = 'M'
    hard_level = 'H'

    difficulty_CHOICES = [
        (easy_level, 'Easy'),
        (medium_level, 'Medium'),
        (hard_level, 'Hard'),
    ]

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    text = models.TextField()
    degree = models.PositiveSmallIntegerField()
    difficulty = models.CharField(max_length=1, choices=difficulty_CHOICES, default=medium_level)
    is_multiple = models.BooleanField(default=False)
    is_true_false = models.BooleanField(default=False)
    in_practice = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='questions', null=True, blank=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer')
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
