from django.db import models


class Vk_posts(models.Model):
    id = models.CharField(max_length=15,
                          primary_key=True,
                          verbose_name='ID поста')
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
