import os

import requests
import vk_api
from social_django.models import UserSocialAuth

from django.views.generic import ListView
from django.db.models import Q
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .models import Vk_posts
from .forms import CreatePostForm

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
    template_name = 'animals/index.html' # 'vk_posts/vk_posts.html'  # поправить при мерже в main
    context_object_name = 'cat'

    def get_queryset(self):
        """Функция выводить все записи с упоминание котов"""
        list_cat = Vk_posts.objects.filter(
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


class PostCreate(CreateView):
    form_class = CreatePostForm
    success_url = reverse_lazy('vk_posts:cat_list')
    template_name = 'vk_posts/vk_posts.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        social_user = UserSocialAuth.objects.get(user=self.request.user)

        access_token = social_user.extra_data['access_token']
        response = requests.get('https://api.vk.com/method/wall.post?', params={
            'access_token': access_token,
            'v': 5.131,
            'owner_id': -217638481,
            'from_group': 1,
            'message': 'из джанго!!!',
        })
        # response = requests.get('https://api.vk.com/method/wall.get?',
        #                         params={'access_token': access_token,
        #                                 'v': 5.131,
        #                                 'owner_id': 261945461})
        # response = requests.get('https://oauth.vk.com/authorize',
        #                         params={
        #                             'client_id': 51509590,
        #                             'scope': 1073737727,
        #                             'redirect_uri': 'http://api.vk.com/blank.html',
        #                         })
        print(response.text)
        return super(PostCreate, self).form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     pass
