from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.core.paginator import Paginator
from django.db.models import Count

from .forms import PostForm
from .models import Category, MainAnimals


class AnimalList(ListView):
    queryset = MainAnimals.objects.all()[:15]
    context_object_name ='animal'
    paginate_by = 7
    extra_context = {'title': 'Главная'}
    template_name ='animals/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return MainAnimals.objects.filter(is_publish=True,)


class CategoryList(ListView):
    queryset = Category
    context_object_name = 'animal'
    template_name = 'animals/category.html'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return MainAnimals.objects.filter(category_id=self.kwargs['category_id'], is_publish=True)


class AnimalPostDetail(DetailView):
    model = MainAnimals
    template_name = 'animals/detail_post.html'
    context_object_name = 'ani'
    slug_url_kwarg = 'animals_slug'


class CreatView(CreateView):
    form_class = PostForm 
    template_name = 'animals/forms_post.html'





   
   
