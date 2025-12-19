from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson
from users.managers import UserManager


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name='email',
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name='Номер телефона',
    )
    city = models.CharField(
        max_length=30,
        verbose_name='город',
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name='аватар'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        db_table = 'Users'


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='пользователь'
    )
    paid_at = models.DateField(
        auto_now_add=True,
        verbose_name='Дата платежа'
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Курс',
        null=True,
        blank=True
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Урок',
        null=True,
        blank=True
    )
    amount = models.IntegerField(
        verbose_name='Сумма'
    )
    payment_method = models.CharField(
        max_length=15,
        choices=[
            ('cash', 'Наличная'),
            ('cashless', 'Безналичная'),
        ],
        verbose_name='метод оплаты'
    )

    def __str__(self):
        return f'Оплатил: {self.user}, сумма: {self.amount}'

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
        db_table = "Payment"
