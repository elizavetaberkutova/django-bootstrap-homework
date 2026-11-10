
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    # Головна сторінка
    path('', views.index, name='index'),

    # Сторінка поста за slug (старий маршрут)
    path(
        'post/<slug:post_slug>',
        views.get_post,
        name='post_detail'
    ),

    # Сторінка поста за ID (нове завдання)
    path(
        'post/id/<int:post_id>/',
        views.post_detail,
        name='post_detail_id'
    ),

    # Профіль автора
    path(
        'profile/<int:user_id>/',
        views.profile_detail,
        name='profile_detail'
    ),

    # Контакти
    path('contact/', views.contact, name='contact'),

# Підписка на новини
path('subscribe/', views.subscribe, name='subscribe'),

    # Створення поста
    path(
        'posts/create/',
        views.post_create,
        name='post_create'
    ),

    # Редагування поста
    path(
        'posts/update/<int:id>',
        views.post_update,
        name='post_update'
    ),

    # Реєстрація
    path('register/', views.register, name='register'),

    # Вхід
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    # Вихід
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
]
