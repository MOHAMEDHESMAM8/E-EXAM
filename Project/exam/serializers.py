from abc import ABC

from rest_framework import serializers

from exam.models import Exam, ExamOptions


class ExamSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    total = serializers.IntegerField()
    time = serializers.TimeField()
    created_at = serializers.DateField()


class chaptersSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    exam = ExamSerializers(many=True, read_only=True)


class ExamOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamOptions
        fields = ['count', 'difficulty', 'chapter']


class CreateExamSerializers(serializers.ModelSerializer):
    exam_options = ExamOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['name', 'time', 'chapter','exam_options']

    def create(self, validated_data, **kwargs):
        exam_options = validated_data.pop('exam_options')
        exam = Exam()
        exam.name = validated_data.pop('name')
        exam.time = validated_data.pop('time')
        exam.chapter = validated_data.pop('chapter')
        exam.save()
        return exam
