from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
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
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        db_table = 'Users'
