import datetime

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User

COUNT_ELEMS = 10


@login_required
def index(request):
    author = User.objects.get(username='leo')
    start_date = datetime.date(1854, 7, 7)
    end_date = datetime.date(1854, 7, 21)
    keyword = ''
    template = 'posts/index.html'
    post_list = (Post.objects
                 .filter(text__contains=keyword)
                 .filter(author=author)
                 .filter(pub_date__range=(start_date, end_date))
                 )
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)


@login_required
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = user.posts.all()
    count_posts = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'count_posts': count_posts,
        'user': user,
    }
    return render(request, 'posts/profile.html', context)


@login_required
def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post = get_object_or_404(Post, pk=post_id)
    user = get_object_or_404(User, username=post.author)
    count_posts = user.posts.count()
    context = {
        'post': post,
        'count_posts': count_posts,
    }
    return render(request, 'posts/post_detail.html', context)
