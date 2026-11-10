
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Comment, Subscriber

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'category', 'tags')
        widgets = {}
        labels = {'title': 'Заголовок'}


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Напишіть коментар...'
            })
        }

    def clean_text(self):
        text = self.cleaned_data['text'].strip()

        if len(text) < 5:
            raise forms.ValidationError(
                'Коментар повинен містити мінімум 5 символів.'
            )

        if len(text) > 500:
            raise forms.ValidationError(
                'Коментар не може перевищувати 500 символів.'
            )

        return text


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть ваш email'
            })
        }

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if Subscriber.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'Цей email вже підписаний на новини.'
            )

        return email
