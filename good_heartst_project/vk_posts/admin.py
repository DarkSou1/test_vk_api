from django.contrib import admin

from .models import Vk_posts


@admin.register(Vk_posts)
class AdminVkPosts(admin.ModelAdmin):
    list_display = ('id',
                    'date',
                    'text_post',
                    'photo')
