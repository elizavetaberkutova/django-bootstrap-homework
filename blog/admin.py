from django.contrib import admin
from .models import Post, Category,Tag



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published_date', 'user','content_length']
    list_filter = ['category', 'published_date']
    search_fields = ['title', 'content']
    ordering = ('-published_date',)
    list_per_page = 10

    @admin.display(description="Довжина тексту")
    def content_length(self,obj):
        return len(obj.content)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name',]
    search_fields = ['name']
    ordering = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id','name',]
    search_fields = ['name']
    ordering = ('name',)

