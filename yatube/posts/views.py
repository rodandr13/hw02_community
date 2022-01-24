from django.shortcuts import render, get_object_or_404

from .models import Post, Group

COUNT_ELEMS = 10


def index(request):
    posts = Post.objects.order_by('-pub_date')[:COUNT_ELEMS]
    template = 'posts/index.html'
    context = {
        'posts': posts
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:COUNT_ELEMS]
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)
