from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from study.models import Course, Lesson, Payment, Subscription
from study.validators import VideoUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoUrlValidator(field='video_url')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()
    lesson = LessonSerializer(read_only=True, many=True)
    is_subscribed = SerializerMethodField()

    def get_lessons_count(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, course):
        user = self.context['request'].user
        subscription = Subscription.objects.filter(course=course.id, user=user.id)
        if subscription:
            return True
        return False

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
