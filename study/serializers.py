from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from study.models import Course, Lesson, Payment, Subscription
from study.validators import VideoUrlValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор модели урока"""

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoUrlValidator(field='video_url')]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор модели курса"""
    lessons_count = SerializerMethodField()
    lesson = LessonSerializer(read_only=True, many=True)
    is_subscribed = SerializerMethodField()

    def get_lessons_count(self, course):
        """Колличество уроков в курсе"""
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, course):
        """Наличие подписки у текущего пользователя"""
        user = self.context['request'].user
        subscription = Subscription.objects.filter(course=course.id, user=user.id)
        if subscription:
            return True
        return False

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор модели платежей"""
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор модели подписки"""
    class Meta:
        model = Subscription
        fields = '__all__'
