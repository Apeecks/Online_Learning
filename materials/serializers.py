from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializers(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ("owner",)


class CourseSerializers(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializers(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ("owner",)

    def get_lessons_count(self, instance):
        return instance.lessons.all().count()
