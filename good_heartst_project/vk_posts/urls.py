from django.urls import path
from .views import AnimalList, DogView, DogSearchHome, CatSearchHome

app_name = 'vk_posts'

urlpatterns = [
    path('', AnimalList.as_view(), name='cat_list'),
    path('dog/', DogView.as_view(), name='dog_list'),
    path('dog_search/', DogSearchHome.as_view(), name='Dog_search'),
    path('cat_search/', CatSearchHome.as_view(), name='Cat_search'),
]