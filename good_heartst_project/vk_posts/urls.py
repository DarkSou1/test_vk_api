from django.urls import path
from .views import VkPostsList

app_name = 'vk_posts'

urlpatterns = [
    path('', VkPostsList.as_view(), name='vk_posts'),
]