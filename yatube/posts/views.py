from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User
from .forms import PostForm

COUNT_ELEMS = 10


@login_required
def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all()
    paginator = Paginator(post_list, COUNT_ELEMS)
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
    paginator = Paginator(post_list, COUNT_ELEMS)
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
    template = 'posts/profile.html'
    user = get_object_or_404(User, username=username)
    post_list = user.posts.all()
    count_posts = post_list.count()
    paginator = Paginator(post_list, COUNT_ELEMS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'count_posts': count_posts,
        'user': user,
    }
    return render(request, template, context)


@login_required
def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    user = get_object_or_404(User, username=post.author)
    count_posts = user.posts.count()
    context = {
        'post': post,
        'count_posts': count_posts,
    }
    return render(request, template, context)


def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            new_post = form.save(commit=False)
            new_post.author = request.user
            form.save()
            return redirect(f'/profile/{request.user}/')
        return render(request, template, context)
    return render(request, template, context)


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    template = 'posts/create_post.html'
    context = {
        'post': post
    }
    if request.method == 'GET':
        is_edit = True
        form = PostForm(post)
        context = {
            'post': post,
            'form': form,
            'is_edit': is_edit,
        }
    if request.method == 'POST':
        form = PostForm(request.POST, post)
        if form.is_valid():
            form.save()
        return redirect('posts:post_detail', post_id=post_id)
    return render(request, template, context)

