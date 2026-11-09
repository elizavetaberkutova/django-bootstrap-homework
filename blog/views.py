
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import PostForm, RegisterForm
from .models import Post, Category, Tag


def get_categories():
    categories = list(Category.objects.all())
    middle = (len(categories) + 1) // 2

    return {
        'categories': categories[:middle],
        'categories2': categories[middle:],
    }


def index(request):
    posts = Post.objects.all()
    tags = Tag.objects.all()

    category_id = request.GET.get('category', '')
    tag_id = request.GET.get('tag', '')
    query = request.GET.get('q', '').strip()

    if category_id.isdigit():
        posts = posts.filter(category_id=int(category_id))

    if tag_id.isdigit():
        posts = posts.filter(tags__id=int(tag_id))

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    posts = posts.distinct()

    context = {
        'posts': posts,
        'tags': tags,
        'query': query,
        'selected_category': category_id,
        'selected_tag': tag_id,
    }

    context.update(get_categories())

    return render(request, 'blog/index.html', context)


def get_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)

    context = {
        'post': post,
        'tags': Tag.objects.all(),
    }

    context.update(get_categories())

    return render(request, 'blog/post.html', context)


def contact(request):
    context = {
        'tags': Tag.objects.all(),
    }

    context.update(get_categories())

    return render(request, 'blog/contact.html', context)


@login_required(login_url='blog:login')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()

            return redirect('blog:index')
    else:
        form = PostForm()

    return render(
        request,
        'blog/post_create.html',
        {'form': form}
    )


@login_required(login_url='blog:login')
def post_update(request, id):
    post = get_object_or_404(
        Post,
        id=id,
        user=request.user
    )

    if request.method == 'POST':
        form = PostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():
            form.save()
            return redirect('blog:index')
    else:
        form = PostForm(instance=post)

    return render(
        request,
        'blog/post_update.html',
        {'form': form, 'post': post}
    )


def register(request):
    if request.user.is_authenticated:
        return redirect('blog:index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('blog:index')
    else:
        form = RegisterForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )

