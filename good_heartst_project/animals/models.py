from importlib.resources import contents
from django.db import models
from django.urls import reverse
# from django.contrib.auth.models import MyUser

from users.models import MyUser


class MainAnimals(models.Model):
    """то как будут отброжаться новостнные новости и все посты и главные новости"""
    title = models.CharField(
        max_length=150,
        verbose_name='Название'
    )

    contents = models.TextField(
        blank=True,
        verbose_name='Контекст',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    update_up = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    is_publish = models.BooleanField(
        default=True,
        verbose_name='Опубликовать'
    )
    potho = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name='Фото'
    )
    url = models.URLField(blank=True)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name="URL")
    author = models.ForeignKey(
        MyUser,
        on_delete=models.PROTECT,
        verbose_name='Автор', )
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse('animals:detail',
                       kwargs={'animals_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']


class Category(models.Model):
    category = models.CharField(
        max_length=250,
        verbose_name='Категория',
        db_index=True
    )

    def get_absolute_url(self):
        """Method for a category that specifies a specific category"""
        return reverse("category", kwargs={"category_id": self.pk})

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
