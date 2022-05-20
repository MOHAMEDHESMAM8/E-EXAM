from rest_framework import serializers
from exam.models import Exam, ExamOptions, ExamGroups
from user.models import Chapter, Group


class ExamSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    total = serializers.IntegerField()
    time = serializers.TimeField()
    created_at = serializers.DateField()


class ChaptersSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    exam = ExamSerializers(many=True, read_only=True)


class ExamOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamOptions
        fields = ['id', 'count', 'difficulty', 'chapter']


def count_total_questions(exam_options):
    count = 0
    for obj in exam_options:
        count += obj.get('count')
    return count


class GetCreateExamSerializers(serializers.ModelSerializer):
    exam_options = ExamOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['name', 'time', 'chapter', 'exam_options']

    def create(self, validated_data, **kwargs):
        exam_options = validated_data.pop('exam_options')
        exam = Exam()
        exam.name = validated_data.pop('name')
        exam.time = validated_data.pop('time')
        exam.professor = self.context['request'].user.professor
        exam.chapter_id = validated_data.pop('chapter')
        exam.level = validated_data.pop('level')
        exam.total = count_total_questions(exam_options)
        exam.save()
        for obj in exam_options:
            new_obj = ExamOptions()
            new_obj.count = obj.pop('count')
            new_obj.difficulty = obj.pop('difficulty')
            new_obj.chapter_id = obj.pop('chapter')
            new_obj.exam = exam
            new_obj.save()
        return exam


class StudentChaptersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['name']


class StudentExamGroupsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExamGroups
        fields = ['start_at', 'end_at']


class StudentExamSerializers(serializers.ModelSerializer):
    exam_groups = StudentExamGroupsSerializers(source='filtered_group', many=True, read_only=True)
    chapter = StudentChaptersSerializers(read_only=True)

    class Meta:
        model = Exam
        fields = ['name', 'total', 'chapter', 'time', 'exam_groups']

    def to_representation(self, instance):
        data = super(StudentExamSerializers, self).to_representation(instance)
        obj = data.pop('chapter')
        data['chapter_name'] = obj['name']
        group_data = data.pop('exam_groups')
        for key, val in group_data[0].items():
            data.update({key: val})
        return data