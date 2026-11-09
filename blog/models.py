from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок',unique=True)
    content = models.TextField(verbose_name='Вміст')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публікації')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категорія')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    tags = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField(max_length=200,unique=True,blank=True)
    image = models.ImageField(upload_to='posts/',verbose_name='Обкладинка')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Публікація'
        verbose_name_plural = 'Публікації'


