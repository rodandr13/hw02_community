import datetime

from django.shortcuts import render, get_object_or_404

from .models import Post, Group, User

COUNT_ELEMS = 10


def index(request):
    author = User.objects.get(username='leo')
    start_date = datetime.date(1854, 7, 7)
    end_date = datetime.date(1854, 7, 21)
    keyword = "утро"
    posts = (Post.objects
             .filter(text__contains=keyword)
             .filter(author=author)
             .filter(pub_date__range=(start_date, end_date))
             )
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
