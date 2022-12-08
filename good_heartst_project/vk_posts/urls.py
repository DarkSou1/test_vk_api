from django.urls import path
from .views import VkPostsList, AnimalList, DogView, DogSearchHome, CatSearchHome

app_name = 'vk_posts'

urlpatterns = [
    #path('', VkPostsList.as_view(), name='vk_posts'),
    path('', AnimalList.as_view(), name='cat_list'),
    path('dog/', DogView.as_view(), name='dog_list'),
    path('dog_search/', DogSearchHome.as_view(), name='Dog_search'),
    path('cat_search/', CatSearchHome.as_view(), name='Cat_search'),
]