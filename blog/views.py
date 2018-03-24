from django.shortcuts import render

from django.views.generic import ListView
from django.views.generic import DetailView

from .models import Post

class PostListView(ListView):
    model = Post
    # template_name = "blog/list.html"


class PostDetailView(DetailView):
    model = Post
    # template_name = "TEMPLATE_NAME"
