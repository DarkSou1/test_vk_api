from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CreatingForm


class SingUp(CreateView):
    form_class = CreatingForm
    success_url = reverse_lazy('animals:list')
    template_name = 'users/signup.html'

