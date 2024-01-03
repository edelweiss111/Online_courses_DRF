from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from study.models import Course, Lesson, Payment, Subscription
from study.pagination import CourseAndLessonPagination
from study.permissions import IsModerator, IsOwner
from study.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from study.servises import StripeService
from study.tasks import mailing_about_updates
import os

STRIPE_API = os.getenv('STRIPE_API_KEY')


class CourseViewSet(viewsets.ModelViewSet):
    """Вьюсет модели курса"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CourseAndLessonPagination

    def get_permissions(self):
        """Разрешения для разных типов запроса"""
        if self.action == 'create':
            permission_classes = [~IsModerator]
        elif self.action == 'retrieve' or 'update':
            permission_classes = [IsModerator | IsOwner]
        elif self.action == 'destroy':
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Присваивание пользователя к курсу"""
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        course = serializer.save()
        mailing_about_updates.delay(course.pk)


class LessonCreateAPIView(generics.CreateAPIView):
    """Эндпоинт для создания урока"""
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator]

    def perform_create(self, serializer):
        """Присваивание владельца к уроку"""
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Эндпоинт для вывода списка уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CourseAndLessonPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Эндпоинт для вывода урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт для редактирования урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]

    def perform_update(self, serializer):
        lesson = serializer.save()
        mailing_about_updates.delay(lesson.course.pk)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт для удаления урока"""
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class PaymentListAPIView(generics.ListAPIView):
    """Эндпоинт для вывода списка платежей"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson']
    ordering_fields = ['pay_date']


class PayLessonAPIView(generics.CreateAPIView):
    """Эндпоинт для создания платежа на урок"""
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        new_payment = serializer.save()
        new_payment.user = self.request.user
        lesson_pk = self.kwargs.get('pk')
        new_payment.paid_lesson = Lesson.objects.get(pk=lesson_pk)
        session = StripeService(STRIPE_API).create_payment(new_payment.paid_lesson, new_payment.user)
        new_payment.session_id = session.id
        new_payment.payment_url = session.url
        new_payment.save()


class PayCourseAPIView(generics.CreateAPIView):
    """Эндпоинт для создания на курс"""
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        new_payment = serializer.save()
        new_payment.user = self.request.user
        course_pk = self.kwargs.get('pk')
        new_payment.paid_course = Course.objects.get(pk=course_pk)
        session = StripeService(STRIPE_API).create_payment(new_payment.paid_course, new_payment.user)
        new_payment.session_id = session.id
        new_payment.payment_url = session.url
        new_payment.save()


class CheckPaymentAPIView(generics.RetrieveAPIView):
    """Эндпоинт для проверки платежа"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get_object(self):
        self.object = super().get_object()
        session_id = self.object.session_id
        session = StripeService(STRIPE_API).check_payment(session_id)
        if session.payment_status == 'paid' or session.payment_status == 'complete':
            self.object.is_paid = True
        self.object.save()
        return self.object


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """Эндпоинт для создания подписки"""
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        """Присваивание подписки к текущему курсу и пользователю"""
        new_sub = serializer.save()
        new_sub.user = self.request.user
        course_pk = self.kwargs.get('pk')
        new_sub.course = Course.objects.get(pk=course_pk)
        new_sub.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт для удаления подписки"""
    queryset = Subscription.objects.all()
