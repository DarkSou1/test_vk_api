import os
import requests
import vk_api
from django.db import models
from django.contrib.auth import get_user_model

from .servise import SendWallPost

from dotenv import load_dotenv

from social_django.models import UserSocialAuth
from social_django.utils import load_strategy

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

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     pass
    #     # social_user = UserSocialAuth.objects.get(user=self.author)
        # # print(social_user)
        # print('--------------')
        # print(social_user.extra_data['access_token'])
        # api_method = 'https://api.vk.com/method/wall.post'
        # response = requests.post('https://api.vk.com/method/wall.post', data={
        #     # 'token': os.getenv('ACCESS_TOKEN'),
        #     'token': social_user.extra_data['access_token'],
        #     'v': 5.131,
        #     'owner_id': -217638481,
        #     'from_group': 0,
        #     'message': self.text,
        # })
        # print(response.json())
        # print('--------------')
        # # super().save()

    class Meta:
        verbose_name = 'Модель для постинга в Vk'
        verbose_name_plural = 'Модели для постинга в Vk'
        ordering = ('-id',)
