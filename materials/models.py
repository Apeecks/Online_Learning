from django.conf import settings
from django.db import models


class Course(models.Model):

    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(
        upload_to="course/",
        blank=True,
        null=True,
        verbose_name='курс'
    )
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
        null=True,
        blank=True,
        verbose_name="владелец",
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        db_table = 'Course'


class Lesson(models.Model):

    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(
        upload_to="lesson/",
        blank=True,
        null=True,
        verbose_name='урок'
    )
    url = models.URLField(
        verbose_name='url'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='курс',
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lessons",
        null=True,
        blank=True,
        verbose_name="владелец",
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        db_table = 'Lesson'


class CourseSubscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_subscriptions",
        verbose_name="пользователь",
    )
    course = models.ForeignKey(
        "materials.Course",
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="курс",
    )

    class Meta:
        unique_together = ("user", "course")
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
        db_table = 'CourseSubscription'
