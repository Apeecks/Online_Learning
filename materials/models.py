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

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        db_table = 'Lesson'
