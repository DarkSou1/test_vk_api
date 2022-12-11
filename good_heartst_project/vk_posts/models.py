import os

from django.db import models
from django.contrib.auth import get_user_model

from .servise import SendWallPost

from dotenv import load_dotenv

load_dotenv()
User = get_user_model()


class Vk_posts(models.Model):
    id = models.CharField(max_length=15,
                          primary_key=True,
                          verbose_name='ID поста',
                          default='бд дополнит')
    date = models.DateField(auto_now=False,
                            auto_now_add=False,
                            verbose_name='Дата поста')
    text_post = models.TextField(max_length=4096,
                                 verbose_name='Текст поста')
    photo = models.TextField(max_length=4096,
                             verbose_name='Фото поста')

    class Meta:
        verbose_name = 'Модель поста из Vk'
        verbose_name_plural = 'Модели постов из Vk'
        ordering = ('-id',)


class PostToVk(models.Model):
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE,)
    text = models.TextField(verbose_name='Текст поста',
                            blank=False,
                            max_length=4096,)
    photo = models.ImageField(verbose_name='Фото поста',
                              blank=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        author = self.author
        sender = SendWallPost(self.text, author.phone_number, access_token=os.getenv('ACCESS_TOKEN'),)
        sender.send()
        super().save()

    class Meta:
        verbose_name = 'Модель для постинга в Vk'
        verbose_name_plural = 'Модели для постинга в Vk'
        ordering = ('-id',)
