from django.db import models
from django.contrib.auth.models import AbstractUser

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
VETERINARY = 'veterinary'

ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (VETERINARY, 'Ветеринар'),
    (ADMIN, 'Администратор'),
)


class MyUser(AbstractUser):
    """Кастомная модель пользователя."""
    username = models.CharField(verbose_name='Ник пользователя',
                                max_length=100,
                                unique=True)
    email = models.EmailField(verbose_name='Почта пользователя',
                              unique=True,
                              max_length=254,)
    first_name = models.CharField(verbose_name='Имя пользователя',
                                  max_length=150,)
    last_name = models.CharField(verbose_name='Фамилия пользователя',
                                 max_length=150)
    bio = models.TextField(verbose_name='Биография',
                           blank=True)
    role = models.CharField(verbose_name='Роль пользователя',
                            max_length=20,
                            choices=ROLES,
                            default=USER)

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_veterinary(self):
        return self.role == VETERINARY

    @property
    def is_admin(self):
        return self.role == ADMIN

    def __str__(self):
        return self.username
