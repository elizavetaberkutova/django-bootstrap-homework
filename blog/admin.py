
from django.contrib import admin
from .models import Category, Tag, Post, Profile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'birth_date')


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
