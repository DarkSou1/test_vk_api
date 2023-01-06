from django import forms

from .models import PostToVk


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = PostToVk
        fields = ('text', 'photo')
