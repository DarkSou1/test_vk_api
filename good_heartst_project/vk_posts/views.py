from django.views.generic import ListView
from django.db.models import Q

from .models import Vk_posts


# class VkPostsList(ListView):
#     queryset = Vk_posts.objects.all()[:10]
#     context_object_name = 'vk_posts'
#     extra_context = {'title': 'Элиста калмыкия'}
#     template_name = 'vk_posts/vk_posts.html'

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(VkPostsList, self).get_context_data(**kwargs)
#         context['title'] = 'Элиста калмыкия'
#         return context

#     def get_queryset(self):
#         return Vk_posts.objects.all()[:10]

class AnimalList(ListView):
    model = Vk_posts
    paginate_by = 10
    extra_context = {'title': 'Главная'}
    template_name = 'vk_posts/cat.html'
    context_object_name = 'cat'


    def  get_queryset(self):
        """Функция выводить все записи с упоминание котов"""
        list_cat = VkPosts.objects.filter(
                                (Q(text_post__icontains='кот') \
                                | Q(text_post__icontains='кош'))\
                                & ~Q(text_post__icontains='соб')
                                )
        return list_cat


class DogView(ListView):
    model = Vk_posts
    paginate_by = 10
    extra_context = {'title': 'Главная'}
    context_object_name = 'dog'
    template_name = 'vk_posts/dog.html'

    def get_queryset(self):
        """Функция выводить все записи с упоминание собак"""
        list_dog = Vk_posts.objects.filter(
                                Q(text_post__icontains='соб')\
                                & (~Q(text_post__icontains='кот')\
                                | ~Q(text_post__icontains='кош'))
                                )
        return list_dog


class DogSearchHome(ListView):
    model = Vk_posts
    paginate_by = 10
    extra_context = {'title': 'Главная'}
    context_object_name = 'dog'
    template_name = 'vk_posts/dog_search.html'

    def get_queryset(self):
        dog_search = Vk_posts.objects.filter((Q(text_post__icontains='соб') \
                                             | Q(text_post__icontains='щен')) \
                                            & (~Q(text_post__icontains='кот') \
                                                | ~Q(text_post__icontains='кош')) \
                                            & ((Q(text_post__icontains='ищет') \
                                                & Q(text_post__icontains='дом')) \
                                                | (Q(text_post__icontains='отда') \
                                                | Q(text_post__icontains='приют')\
                                                | Q(text_post__icontains='взять')))
                                            )
        return dog_search


class CatSearchHome(ListView):
    model = Vk_posts
    paginate_by = 10
    extra_context = {'title': 'Главная'}
    context_object_name = 'cat'
    template_name = 'vk_posts/cat_search.html'
    """дописываю, выдает неправильно данные """
    def get_queryset(self):
        cat_search = Vk_posts.objects.filter((Q(text_post__icontains='кот') | Q(text_post__icontains='кош')) & Q(
            text_post__icontains='отд'))
        return cat_search

