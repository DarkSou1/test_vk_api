from django.views.generic import ListView

from .models import Vk_posts


class VkPostsList(ListView):
    queryset = Vk_posts.objects.all()[:10]
    context_object_name = 'vk_posts'
    extra_context = {'title': 'Элиста калмыкия'}
    template_name = 'vk_posts/vk_posts.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VkPostsList, self).get_context_data(**kwargs)
        context['title'] = 'Элиста калмыкия'
        return context

    def get_queryset(self):
        return Vk_posts.objects.all()[:10]
