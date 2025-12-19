from rest_framework import serializers

from materials.models import Course, Lesson, CourseSubscription
from materials.validators import validate_youtube_url, NoExternalLinksValidator


class LessonSerializers(serializers.ModelSerializer):
    url = serializers.URLField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ("owner",)
        validators = [
            NoExternalLinksValidator(field="description"),
            NoExternalLinksValidator(field="title"),
        ]


class CourseSerializers(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializers(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ("owner",)
        validators = [
            NoExternalLinksValidator(field="description"),
            NoExternalLinksValidator(field="title"),
        ]

    def get_lessons_count(self, instance):
        return instance.lessons.all().count()

    def get_is_subscribed(self, instance):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return CourseSubscription.objects.filter(user=request.user, course=instance).exists()
