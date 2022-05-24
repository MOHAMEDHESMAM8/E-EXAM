from rest_framework import serializers
from exam.models import Exam, ExamOptions, ExamGroups
from user.models import Chapter, Group


class ExamSerializers(serializers.Serializer):
    id= serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    total = serializers.IntegerField()
    time = serializers.IntegerField()
    created_at = serializers.DateField()


class StudentChaptersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['name']


class ChaptersSerializers(serializers.Serializer):
    id= serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    exam = ExamSerializers(many=True)


class ExamOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamOptions
        fields = ['count', 'difficulty', 'chapter']


def count_total_questions(exam_options):
    count = 0
    for obj in exam_options:
        count += obj.get('count')
    return count

class AddExamToGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamGroups
        fields = ['group', 'start_at', 'end_at']



class GetExamSerializers(serializers.ModelSerializer):
    exam_options = ExamOptionsSerializer(many=True)
    exam_groups = AddExamToGroupSerializer(many=True)
    chapter = StudentChaptersSerializers()
    class Meta:
        model = Exam
        fields = ['id','name', 'time', 'chapter', 'exam_options','exam_groups']
        
    def to_representation(self, instance):
        data = super(GetExamSerializers, self).to_representation(instance)
        data["chapter_name"] =data.pop('chapter').get('name')
        return data

class CreateExamSerializers(serializers.ModelSerializer):
    exam_options = ExamOptionsSerializer(many=True)
    exam_groups = AddExamToGroupSerializer(many=True)
    
    class Meta:
        model = Exam
        fields = ['id','name', 'time', 'chapter', 'exam_options','exam_groups']

    def create(self, validated_data, **kwargs):
        exam_options = validated_data.pop('exam_options')
        exam_groups = validated_data.pop('exam_groups')
        print(exam_groups)
        exam = Exam()
        exam.name = validated_data.pop('name')
        exam.time = validated_data.pop('time')
        exam.professor = self.context['request'].user.professor
        exam.chapter_id = validated_data.pop('chapter')
        exam.level = self.context['level']
        exam.total = count_total_questions(exam_options)
        exam.save()
        for obj in exam_options:
            new_obj = ExamOptions()
            new_obj.count = obj.pop('count')
            new_obj.difficulty = obj.pop('difficulty')
            new_obj.chapter_id = obj.pop('chapter')
            new_obj.exam = exam
            new_obj.save()
        for obj in exam_groups:
            examgroup = ExamGroups()
            examgroup.exam_id =exam.id
            examgroup.group_id= obj.pop('group_id')
            examgroup.start_at = obj.pop('start_at')
            examgroup.end_at = obj.pop('end_at')
            examgroup.save()

        return exam
        
    def update(self, instance, validated_data):
        exam_option = validated_data.pop('exam_options')
        options = (instance.exam_options).all()
        options = list(options)
        
        instance.name = validated_data.get('name', instance.name)
        instance.time = validated_data.get('time', instance.time)
        instance.chapter_id = validated_data.get('chapter', instance.chapter)
        instance.level = validated_data.get('level', instance.level)
        instance.total = count_total_questions(exam_option)
        instance.save()
        for obj in exam_option:
            new_obj = options.pop(0)
            if obj.get('id') is None:
                add_record =ExamOptions()
                add_record.count = obj.get('count')
                add_record.difficulty = obj.get('difficulty')
                add_record.chapter_id = obj.get('chapter')
                add_record.exam = instance
                add_record.save()
            new_obj.count = obj.get('count', new_obj.count)
            new_obj.difficulty = obj.get('difficulty', new_obj.difficulty)
            new_obj.chapter_id = obj.get('chapter', new_obj.chapter_id)
            new_obj.save()
        return instance





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




class StudentAvailableExamSerializer(serializers.Serializer):
    id=serializers.IntegerField(source='exam')
    name=serializers.CharField(max_length=255, source='exam__name')
    start_at = serializers.DateTimeField()
    end_at = serializers.DateTimeField()
    time = serializers.IntegerField(source='exam__time')

class StudentExamHistorySerializer(serializers.Serializer):
    id=serializers.IntegerField(source='exam')
    name = serializers.CharField(max_length=255, source='exam__name')
    total_score = serializers.IntegerField(source='exam__total')
    score = serializers.IntegerField(source='result')

class ExamResultSerializer(serializers.Serializer):
    student_phone = serializers.CharField(max_length=255, source='student__user__phone')
    first_name = serializers.CharField(max_length=255, source='student__user__first_name')
    last_name = serializers.CharField(max_length=255, source='student__user__last_name')
    result = serializers.IntegerField()

class StudentExamDetailsSerializer(serializers.Serializer):
    id=serializers.IntegerField(source='exam')
    name=serializers.CharField(max_length=255, source='exam__name')
    start_at = serializers.DateTimeField()
    end_at = serializers.DateTimeField()
    time = serializers.IntegerField(source='exam__time')
    chapter = serializers.CharField(max_length=255, source='exam__chapter')