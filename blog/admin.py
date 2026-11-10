
from django.contrib import admin
from .models import Category, Tag, Post, Profile, Comment, Subscriber


# Категорії
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# Теги
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# Профілі користувачів
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'birth_date')


# Публікації
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'user',
        'published_date',
    )

    search_fields = ('title', 'content')

    list_filter = ('category', 'published_date')

    filter_horizontal = ('tags',)


# Коментарі
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'author',
        'created_at',
    )

    search_fields = (
        'text',
        'author__username',
    )

    list_filter = ('created_at',)


# Підписники на новини
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'created_at',
    )

    search_fields = ('email',)

    ordering = ('-created_at',)

    list_filter = ('created_at',)
