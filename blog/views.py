
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm, RegisterForm, CommentForm, SubscriberForm
from .models import Post, Category, Tag


# Категорії для меню
def get_categories():
    categories = list(Category.objects.all())
    middle = (len(categories) + 1) // 2

    return {
        'categories': categories[:middle],
        'categories2': categories[middle:],
    }


# Головна сторінка блогу
def index(request):
    posts = Post.objects.select_related(
        'category', 'user'
    ).prefetch_related('tags')

    tags = Tag.objects.all()

    category_id = request.GET.get('category', '')
    tag_id = request.GET.get('tag', '')
    query = request.GET.get('q', '').strip()

    if category_id.isdigit():
        posts = posts.filter(
            category_id=int(category_id)
        )

    if tag_id.isdigit():
        posts = posts.filter(
            tags__id=int(tag_id)
        )

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    context = {
        'posts': posts.distinct(),
        'tags': tags,
        'query': query,
        'selected_category': category_id,
        'selected_tag': tag_id,
    }

    context.update(get_categories())

    return render(
        request,
        'blog/index.html',
        context
    )


# Сторінка публікації та коментарі
def get_post(request, post_slug):
    post = get_object_or_404(
        Post,
        slug=post_slug
    )

    if request.method == 'POST':

        if not request.user.is_authenticated:
            return redirect('blog:login')

        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)

            comment.post = post
            comment.author = request.user

            comment.save()

            return redirect(
                'blog:post_detail',
                post_slug=post.slug
            )

    else:
        form = CommentForm()

    comments = post.comments.select_related(
        'author'
    ).order_by('-created_at')

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'tags': Tag.objects.all(),
    }

    context.update(get_categories())

    return render(
        request,
        'blog/post.html',
        context
    )


# Сторінка публікації за ID
def post_detail(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id
    )

    comments = post.comments.select_related(
        'author'
    ).order_by('-created_at')

    context = {
        'post': post,
        'comments': comments,
        'tags': Tag.objects.all(),
    }

    context.update(get_categories())

    return render(
        request,
        'blog/post_detail.html',
        context
    )


# Профіль автора
def profile_detail(request, user_id):
    User = get_user_model()

    author = get_object_or_404(
        User,
        id=user_id
    )

    posts = Post.objects.filter(
        user=author
    ).order_by('-published_date')

    context = {
        'author': author,
        'posts': posts,
        'tags': Tag.objects.all(),
    }

    context.update(get_categories())

    return render(
        request,
        'blog/profile_detail.html',
        context
    )


# Контакти
def contact(request):
    context = {
        'tags': Tag.objects.all(),
    }

    context.update(get_categories())

    return render(
        request,
        'blog/contact.html',
        context
    )


# Створення публікації
@login_required(login_url='blog:login')
def post_create(request):

    if request.method == 'POST':
        form = PostForm(
            request.POST,
            request.FILES
        )

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


# Редагування публікації
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
        form = PostForm(
            instance=post
        )

    return render(
        request,
        'blog/post_update.html',
        {
            'form': form,
            'post': post
        }
    )


# Реєстрація користувача
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


def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)

        if form.is_valid():
            form.save()
            return render(
                request,
                'blog/subscribe.html',
                {'success': True}
            )
    else:
        form = SubscriberForm()

    return render(
        request,
        'blog/subscribe.html',
        {'form': form}
    )
