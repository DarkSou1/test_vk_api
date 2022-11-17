from django.apps import AppConfig


class VkPostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vk_posts'

    def ready(self):
        print('Запуск скрипта!')
        import vk_posts.servise
