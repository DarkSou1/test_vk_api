from django.contrib import admin

from .models import Vk_posts, PostToVk


@admin.register(Vk_posts)
class AdminVkPosts(admin.ModelAdmin):
    list_display = ('id',
                    'date',
                    'text_post',
                    'photo')


@admin.register(PostToVk)
class AbminPostToVk(admin.ModelAdmin):
    list_display = ('id',
                    'author',
                    'text',
                    'photo')
